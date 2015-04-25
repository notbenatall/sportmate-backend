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

import mmglue

import modules.sports.models as models
import modules.sports.messages as messages
import modules.sports.actions as actions


class TestModelToMessageConvert(object):

	def test_sport_category(self):

		cat1 = models.SportCategory(name='Ball')

		cat2 = models.SportCategory(name='Basket Ball')
		cat2.add_parent(cat1)

		cat3 = models.SportCategory(name='Extreme Basket Ball')
		cat3.add_parent(cat2)

		msg = actions.sport_category_to_message(cat3)

		assert msg.name == 'Extreme Basket Ball'
		assert msg.paths[0] == 'ball/basket ball'