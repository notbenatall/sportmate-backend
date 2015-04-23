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

import modules.dummydata.actions as actions
import modules.sports as sports
import modules.sports.actions
import modules.sports.models


class TestDummyData(HRDatastoreTest):

	def setup(self):
		super(TestDummyData, self).setup()
		actions.dummy_data_create()


	def test_create_categories(self):

		cat = sports.models.SportCategory.get_by_name("basket ball")


		assert cat.name == 'Basket Ball'


class TestDummyData2(DatastoreTest):

	def setup(self):
		super(TestDummyData2, self).setup()
		actions.dummy_data_create()


	def test_create_lots_of_games(self):

		games = sports.models.Game.query().fetch()


		assert len(games) == 20