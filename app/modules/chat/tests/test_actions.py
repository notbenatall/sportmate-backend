import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.ext.db import BadValueError
import random

from testtools import DatastoreTest, HRDatastoreTest

from modules.users.models import User
import modules.chat.models as models
import modules.chat.messages as message
import modules.chat.actions as actions

class TestGeneral(DatastoreTest):

	def test_model_to_chat_message():

		user = User(first_name="Adrian", full_name="Adrian Letchford")
		user.put()

		model = models.ChatMessage(
			body="hello",
			recipients="123,456",
			sender_id=3452,
			sender_first_name="Adrian",
			sender_last_name="Letchford",
			sender_profile_image="image")

		msg = actions.model_to_chat_message(model)

		assert msg.sender_id == 3452
		assert msg.body == "hello"
		assert msg.recipients == [123, 456]


class TestGeneral(HRDatastoreTest):

	def test_chat_message_to_model(self):

		user = User(first_name="me", full_name="me too", facebook_id=976)
		user.initialise_new_token()
		user.put()

		msg = message.AuthChatMessage(
			body="hello",
			token=user.get_token(),
			recipients=[123, 456])

		model = actions.auth_chat_message_to_model(msg, user)

		assert model.sender_id == user.key.id()
		assert model.body == "hello"
		assert model.recipients == "123,456"



	def test_add_message(self):

		user = User(first_name="me", full_name="me too", facebook_id=87654)
		user.initialise_new_token()
		user.put()

		parent_key = ndb.Key("some_kind1", "some_id2")

		msg = message.AuthChatMessage(
			body="hello!", 
			token=user.get_token(),
			recipients = [3452746],
			parent_key=parent_key.urlsafe())

		actions.add_message(msg, user)

		thread = models.Thread.get_by_key(parent_key, 1)

		assert thread.messages[0].body == "hello!"
		assert thread.messages[0].sender_id == user.key.id()


	def test_get_messages(self):

		user = User(first_name="me", full_name="me too", facebook_id=8765)
		user.initialise_new_token()
		user.put()

		parent_key = ndb.Key("some_kind3", "some_id3")

		actions.add_message(message.AuthChatMessage(
			body="hello!", 
			recipients = [3452746],
			message_id="563",
			parent_key=parent_key.urlsafe()), user)

		actions.add_message(message.AuthChatMessage(
			body="what's up?", 
			recipients = [3452746],
			message_id="08764",
			parent_key=parent_key.urlsafe()), user)

		msg = actions.get_messages(parent_key)

		assert msg.messages[0].body == "hello!"
		assert msg.messages[1].body == "what's up?"



	def test_get_user_thread_key(self):
		auth_user = User(key=ndb.Key('User', 1))
		other_user = User(key=ndb.Key('User', 2))

		thread = actions.get_two_user_thread(auth_user, other_user)

		assert len(thread.participants) == 2
		assert type(thread.key) is str




