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

from testtools import DatastoreTest

import modules.users.models as usermodels
import modules.chat.models as models


class TestThreadModel(DatastoreTest):

	def test_make_group_parent(self):
		keys = []
		for i in range(1, 5):
			keys.append(ndb.Key(usermodels.User, i))

		key1 = models.Thread.make_private_group_parent(keys)
		random.shuffle(keys)
		key2 = models.Thread.make_private_group_parent(keys)

		assert key1 == key2

	def test_make_key_from_parent(self):
		
		parent_key = ndb.Key("some_kind", "some_id")

		key = models.Thread.make_key_from_parent(parent_key, 45)

		assert key.parent() == parent_key
		assert key.id() == 45


	def test_get_current_thread_number(self):

		parent_key = ndb.Key("some_kind", "some_id")
		models.Thread(key=models.Thread.make_key_from_parent(parent_key, 45)).put()
		models.Thread(key=models.Thread.make_key_from_parent(parent_key, 105)).put()
		models.Thread(key=models.Thread.make_key_from_parent(parent_key, 3)).put()

		number = models.Thread.get_current_thread_number(parent_key)

		assert number == 105


	def test_get_by_key(self):

		parent_key = ndb.Key("some_kind", "some_id")
		models.Thread(key=models.Thread.make_key_from_parent(parent_key, 45)).put()

		thread = models.Thread.get_by_key(parent_key, 45)

		assert thread.key.id() == 45


	def test_add_message(self):

		parent_key = ndb.Key("some_kind", "some_id")
		user_key = ndb.Key(usermodels.User, 5433)
		recipient = 3452746

		message = models.ChatMessage(body="hello!", sender_id=user_key.id())
		message.add_recipient(recipient)

		models.Thread.add_message(parent_key, message)

		thread = models.Thread.get_by_key(parent_key, 1)

		assert thread.messages[0].body == "hello!"

		


