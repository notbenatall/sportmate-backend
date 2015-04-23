import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime
import endpoints
from google.appengine.ext.db import BadValueError
from endpoints import UnauthorizedException, NotFoundException
from testtools import DatastoreTest, HRDatastoreTest

from modules.misc.messages import VoidMessage
import modules.dummydata.api
import modules.sports as sports
import modules.sports.actions

class APITest(DatastoreTest):
	def setup(self):

		super(APITest, self).setup()

		# Expose the api
		self.api = modules.dummydata.api.DummyData()


class TestDummyData(APITest):

	def test_create_dummy_data(self):

		response = self.api.create_dummy_data(VoidMessage())

		assert response.text == "Done!"

		categories = sports.actions.get_all_categories().categories

		assert len(categories) > 0
