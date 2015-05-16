"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds all the models.
"""
# pylint: disable=too-few-public-methods

from google.appengine.ext import ndb
from modules.users.models import User


class ChatMessage(ndb.Model):
	"""
	recipients is a comma separated string of user ids.
	"""
	body = ndb.StringProperty(indexed=False)
	recipients = ndb.StringProperty(indexed=False, required=True)
	message_id = ndb.StringProperty(indexed=False, required=True)
	sender_first_name = ndb.StringProperty(indexed=False, required=True)
	sender_full_name = ndb.StringProperty(indexed=False, required=True)
	sender_profile_image = ndb.StringProperty(indexed=False, required=True)
	sender_id = ndb.IntegerProperty(indexed=False, required=True)

	def add_recipient(self, user_id):
		"""Adds a recipient to this chat message."""
		if self.recipients is None or len(self.recipients) == 0:
			self.recipients = str(user_id)
		else:
			self.recipients += "," + str(user_id)


# class ThreadDetails(ndb.Model):
# 	"""Keeps track of a thread."""
# 	participants = ndb.KeyProperty(User, repeated=True)


class Thread(ndb.Model):
	"""
	Key:
	[Game Key, (Thread, number)] or
	[(?, group_id), (Thread, number)]
	"""
	messages = ndb.StructuredProperty(ChatMessage, repeated=True)

	def is_full(self):
		"""Determines if the thread is full."""
		if len(self.messages) >= 5000:
			return True
		return False


	@staticmethod
	def make_private_group_parent(user_keys):
		"""
		Creates a group parent key from multiple users. The key contains all
		users as kinds. The users are sorted before creating the key such that
		make_private_group_parent(user_keys) ==
		make_private_group_parent(shuffle(user_keys)).
		"""
		user_ids = [key.id() for key in user_keys]
		user_ids.sort()

		pairs = [(User, ID) for ID in user_ids]

		key = ndb.Key(pairs=pairs)

		return key


	@staticmethod
	def make_key_from_parent(parent_key, number):
		"""
		Makes a key from a parent_key and a number. The parent key represents
		the thread ID. The number is the page.
		"""
		pairs = list(parent_key.pairs())
		pairs.append((Thread, number))
		return ndb.Key(pairs=pairs)


	@staticmethod
	def get_current_thread_number(parent_key):
		"""
		Makes a key from a parent_key and a number. The parent key represents
		the thread ID. The number is the page.
		"""

		thread_keys = Thread.query(ancestor=parent_key).fetch(keys_only=True)
		if len(thread_keys) == 0:
			return None

		thread_ids = [key.id() for key in thread_keys]
		thread_ids.sort()

		return thread_ids[-1]

	@staticmethod
	def get_by_key(parent_key, number):
		"""Returns the thread for the given parent and number."""
		pairs = list(parent_key.pairs()) + [(Thread, number)]
		key = ndb.Key(pairs=pairs)
		thread = key.get()
		return thread

	@staticmethod
	def add_message(parent_key, message):
		"""Add a message to the system."""
		number = Thread.get_current_thread_number(parent_key)

		if number is None:
			pairs = list(parent_key.pairs()) + [(Thread, 1)]
			thread = Thread(key=ndb.Key(pairs=pairs))
		else:
			thread = Thread.get_by_key(parent_key, number)

		# If this thread is full, create another one
		if thread.is_full():
			pairs = list(parent_key.pairs()) + [(Thread, thread.key.id()+1)] #pylint: disable=maybe-no-member
			thread = Thread(key=ndb.Key(pairs=pairs))

		thread.messages.append(message)
		thread.put()  #pylint: disable=maybe-no-member