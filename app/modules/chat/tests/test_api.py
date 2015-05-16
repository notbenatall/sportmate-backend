import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime
import endpoints
from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from endpoints import UnauthorizedException, NotFoundException
from testtools import DatastoreTest, HRDatastoreTest

from modules.users.models import User
from modules.users.messages import UserId

import modules.chat.models as models
import modules.chat.actions as actions
import modules.chat.messages as messages
import chat.api

class TestAPI(HRDatastoreTest):
	def setup(self):

		super(TestAPI, self).setup()

		# Expose the api
		self.api = chat.api.Chat()



class TestAddMessage(TestAPI):

	def test(self):

		user = User(first_name="me", full_name="me too", facebook_id=8766)
		user.initialise_new_token()
		user.put()

		parent_key = ndb.Key("some_kind1", "some_id2")

		msg = messages.AuthChatMessage(
			body="hello!", 
			token=user.get_token(),
			recipients = [3452746],
			parent_key=parent_key.urlsafe())

		msg = self.api.add_message(msg)

		thread = models.Thread.get_by_key(parent_key, 1)

		assert thread.messages[0].body == "hello!"
		assert thread.messages[0].sender_id == user.key.id()

		assert msg.sender_id == user.key.id()

class TestGetMessages(TestAPI):

	def test_get_messages(self):

			user = User(first_name="me", full_name="me too", facebook_id=8766)
			user.initialise_new_token()
			user.put()

			parent_key = ndb.Key("some_kind3", "some_id3")

			self.api.add_message(messages.AuthChatMessage(
				body="hello!", 
				recipients = [3452746],
				token=user.get_token(),
				parent_key=parent_key.urlsafe()))

			self.api.add_message(messages.AuthChatMessage(
				body="what's up?", 
				recipients = [3452746],
				token=user.get_token(),
				parent_key=parent_key.urlsafe()))

			msg = self.api.get_messages(messages.ChatMessageRequest(
				token=user.get_token(),
				parent_key=parent_key.urlsafe()))

			assert msg.messages[0].body == "hello!"
			assert msg.messages[1].body == "what's up?"


class TestGetMessages(TestAPI):

	def test_get_user_thread_key(self):

		user = User(first_name="Adrian", full_name="Adrian Letchford", facebook_id=8766)
		user.initialise_new_token()
		user.put()

		user2 = User(first_name="Benjamin", full_name="Benjamin Letchford", facebook_id=87668)
		user2.initialise_new_token()
		user2.put()

		msg = UserId(token=user.get_token(), user=user2.key.id())

		thread = self.api.get_user_thread_key(msg)		

		assert len(thread.participants) == 2
		assert "Adrian Letchford" in [u.full_name for u in thread.participants]
		assert type(thread.key) is str
		assert len(thread.key) > 10