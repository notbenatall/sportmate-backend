"""
Sportmate API v1

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds the models for users.
"""

from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from Crypto.Hash import SHA
import misc # sportmate's misc module

class User(ndb.Model):
	"""Models a User."""

	dumb_token = ndb.StringProperty(indexed=True)
	searchable_name = ndb.StringProperty(indexed=True, required=True)

	full_name = ndb.StringProperty(indexed=False, required=True)
	email = ndb.StringProperty(indexed=False, required=False)

	@staticmethod
	def generate_token(salt):
		"""Generates a random token."""
		sha = SHA.new()
		sha.update(salt)
		sha.update(misc.random_string())
		token = sha.hexdigest()
		return token

	def initialise_new_token(self):
		"""Creates a new token for the user."""
		self.dumb_token = self.generate_token(str(self.key))
		return self.dumb_token

	def get_token(self):
		"""Returns the token for this user."""
		return self.key.urlsafe() + "::" + self.dumb_token

	@staticmethod
	def get_from_token(token):
		"""Gets the user associated with the given token."""
		urlsafe, dumb_token = token.split("::")

		key = ndb.Key(urlsafe=urlsafe)

		try:
			user = key.get()
		except ValueError:
			return None

		if user is None:
			return None

		if user.dumb_token != dumb_token:
			return None

		return user

	def put(self):
		"""Overrides the default put() behaviour to setup automatic fields."""

		# Set the searchable name
		if self.full_name is None:
			raise BadValueError
		self.searchable_name = self.full_name.lower()

		super(User, self).put()


class Relationship(ndb.Model):
	"""
	Models the relationship between two users.
	"""

	users = ndb.KeyProperty(kind=User, indexed=True, repeated=True)
	is_friends = ndb.BooleanProperty(indexed=True, default=False)

	friend_request_sent = ndb.BooleanProperty(indexed=False, default=False)
	friend_request_sender = ndb.KeyProperty(kind=User, indexed=False)
	friend_request_rejected = ndb.BooleanProperty(indexed=False, default=False)
	friend_unfriender = ndb.KeyProperty(kind=User, indexed=False)

	created = ndb.DateTimeProperty(auto_now_add=True)

	def validate(self):
		"""Validates this model."""

		# Make sure this relationship has exactly two users before writing to
		# the database.
		if len(self.users) != 2:
			raise BadValueError

	@staticmethod
	def _key_from_users(user_a, user_b):
		"""
		Creates a Relationship key from two users. The key contains both users
		as kinds. The users are sorted before creating the key such that
		_key_from_users(A, B) == _key_from_users(B, A). This means that the key
		technically does have a parent, but the parent key does not correspond to
		any entities.
		"""
		user_ids = [str(user_a.key.id()), str(user_b.key.id())]
		user_ids.sort()
		key = ndb.Key(User, user_ids[0], User, user_ids[1],
			Relationship, ''.join(user_ids))
		return key

	@staticmethod
	def create(user_a, user_b):
		"""
		Creates a new Relationship between two users. The relationship's key
		prevents the entity from having a parent. See _key_from_users().
		"""
		relationship = Relationship(
			key=Relationship._key_from_users(user_a, user_b),
			users=[user_a.key, user_b.key])
		return relationship

	def put(self):
		"""Overrides the default put() behaviour."""
		self.validate()
		super(Relationship, self).put()

	@staticmethod
	def get_by_users(user_a, user_b):
		"""Returns the relationship between the two users."""

		key = Relationship._key_from_users(user_a, user_b)
		relationship = key.get()
		return relationship



class FriendList(ndb.Model):
	"""
	Stores a list of some of a person's friends for faster and cheaper lookup.
	There is a limit of 5000 on the number of users that can be stored in each
	individual list model. Users with more than 5,000 friends will need to have
	multiple indexes.

	Parent: User
	"""

	friends = ndb.KeyProperty(kind=User, indexed=True, repeated=True)
	full = ndb.BooleanProperty(indexed=True, default=False)

	def validate(self):
		"""Validates this model."""

		misc.validate_parent(self, User)

		if len(self.friends) > 5000:
			raise BadValueError

	def put(self):
		"""Write the friends list to the database after validating."""
		self.validate()
		super(FriendList, self).put()

	def add_friend(self, user):
		"""Add a user to this friend list."""
		if len(self.friends) >= 5000:
			raise Exception("Full.")

		self.friends.append(user)

		if len(self.friends) == 5000:
			self.full = True
		else:
			self.full = False

	@staticmethod
	def get_or_create_addable_friend_list(user):
		"""
		Given a user, returns a friends list that can have at least one more
		user added to it.
		"""
		query = FriendList.query(ancestor=user.key)
		query.filter(FriendList.full == False)
		friend_list = query.get()

		if friend_list is None:
			friend_list = FriendList(parent=user.key)

		return friend_list