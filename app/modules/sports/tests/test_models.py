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

from testtools import DatastoreTest

import users.models as usermodels
import sports.models as models

class TestSportCategoryModel(DatastoreTest):

	@raises(BadValueError)
	def testEmptyPut(self):
		cat = models.SportCategory()
		cat.put()

	def testBasicPut(self):
		cat = models.SportCategory(name='Basket Ball')
		cat.put()

	def testRetrieveByFullName(self):
		cat = models.SportCategory(name='Basket Ball')
		cat.put()
		retrieved_cat = models.SportCategory.get_by_name('Basket Ball')
		assert retrieved_cat == cat

	def test_add_parent(self):
		cat1 = models.SportCategory(name='Ball')

		cat2 = models.SportCategory(name='Basket Ball')
		cat2.add_parent(cat1)

		cat3 = models.SportCategory(name='Extreme Basket Ball')
		cat3.add_parent(cat2)

		assert cat2.paths[0] == 'ball'
		assert cat1.key in cat2.parents
		assert cat3.paths[0] == 'ball/basket ball'
		assert cat2.key in cat3.parents


class TestSportCategoryModelGetAll(DatastoreTest):
	def test(self):

		cat = models.SportCategory(name='Cycling')
		cat.put()

		categories = models.SportCategory.get_all()

		assert len(categories) == 1
		assert categories[0].name == 'Cycling'


class TestGameModel(DatastoreTest):

	def setup(self):
		super(TestGameModel, self).setup()

		self.user = usermodels.User(full_name = 'Rowan Atkinson', first_name="Rowan")
		self.user.put()

		self.cat = models.SportCategory(name='Basketball')
		self.cat.put()

	def testBasicPut(self):
		game = models.Game(
			category = [self.cat.key],
			players_needed=5,
			geo=ndb.GeoPt(37, -122),
			time = datetime.now(),
			parent = self.user.key
			)
		game.put()

	@raises(BadValueError)
	def test_missing_category(self):
		game = models.Game(
			players_needed=5,
			geo=ndb.GeoPt(37, -122),
			time = datetime.now(),
			parent = self.user.key
			)
		game.put()


	def test_update_geohash(self):
		game = models.Game(
			geo=ndb.GeoPt(37, -122),
			)
		game.update_geohash()

		assert type(game.geohash) is str 
		assert len(game.geohash) == 20

	@raises(BadValueError)
	def test_too_many_players(self):
		game = models.Game(
			category = [self.cat.key],
			players_needed=5,
			players_joined=6, # Too many players have joined!
			geo=ndb.GeoPt(37, -122),
			time = datetime.now(),
			parent = self.user.key
			)
		game.put()