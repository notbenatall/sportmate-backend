import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime
import endpoints
from protorpc import message_types
from google.appengine.ext.db import BadValueError
from endpoints import UnauthorizedException, NotFoundException
from testtools import DatastoreTest, HRDatastoreTest

import modules.geo.actions as actions
import modules.geo.messages as messages
import geo.api

class TestAPI(HRDatastoreTest):
	def setup(self):

		super(TestAPI, self).setup()

		# Expose the api
		self.api = geo.api.Geo()



class TestBasic(TestAPI):

	def test(self):


		locations = self.api.get_default_places(message_types.VoidMessage())
		locations = locations.locations

		assert len(locations) > 0
		assert type(locations[0].venue) is str
		assert type(locations[0].subvenue) is str
		assert type(locations[0].lat) is float
		assert type(locations[0].lon) is float

