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
from testtools import DatastoreTest, HRDatastoreTest
from endpoints import NotFoundException

import modules.misc.models as models

class DummyModel(ndb.Model):
	pass

class TestGetModel(DatastoreTest):

	def setup(self):
		super(TestGetModel, self).setup()

		self.dummy = DummyModel()
		self.dummy.put()

	def test_get_model(self):

		a = models.get_model(self.dummy, DummyModel)
		b = models.get_model(self.dummy.key, DummyModel)
		c = models.get_model(self.dummy.key.id(), DummyModel)

		assert self.dummy == a
		assert self.dummy == b
		assert self.dummy == c

	@raises(NotFoundException)
	def test_get_model_not_found(self):
		models.get_model("alskfjadlkfja", DummyModel)