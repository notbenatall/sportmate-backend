import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime, timedelta
import endpoints
from google.appengine.ext.db import BadValueError
from endpoints import UnauthorizedException, NotFoundException
from testtools import DatastoreTest, HRDatastoreTest

from modules.misc.messages import VoidMessage, TextMessage

import modules.admin.actions as actions
import modules.admin.api

from modules.sports.actions import get_all_categories

class APITest(DatastoreTest):
	def setup(self):
		super(APITest, self).setup()

		# Expose the api
		self.api = modules.admin.api.Admin()


class TestGeneral(APITest):

	def test(self):
		self.api.create_new_categories(VoidMessage())
		cats = get_all_categories().categories

		assert len(cats) > 10
