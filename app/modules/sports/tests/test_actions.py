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

import modules.users.models as usermodels
import modules.sports.models as models
import modules.sports.actions as actions
import modules.sports.messages as messages

def test_nothing():
	assert True == True

class TestGeneral(DatastoreTest):

	def test_get_all_sports(self):

		cat1 = models.SportCategory(name='Ball')
		cat1.put()

		cat2 = models.SportCategory(name='Archery')
		cat2.put()

		cat3 = models.SportCategory(name='Football')
		cat3.add_parent(cat1)
		cat3.put()

		everything = actions.get_all_categories()

		assert type(everything) == messages.CategoryList
		assert len(everything.categories) == 3

		assert everything.categories[0].name == 'Archery'
		assert everything.categories[2].name == 'Football'
		assert len(everything.categories[2].parent_ids) == 1
		assert everything.categories[2].parent_ids[0] == cat1.key.id()


	def test_create_new_game(self):

		user = usermodels.User(full_name="Adrian")
		user.put()

		msg = messages.NewGame(
			categories = ["American Football"],
			level = 1,
			time = datetime.now(),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		game = actions.create_new_game(user, msg)

		game = game.key.get()

		assert game.key.parent() == user.key
		assert game.players_needed == 2
		assert game.category[0].id() == "american football"
		assert game.geo.lat == 34
		assert game.geo.lon == 89


class TestListGames(DatastoreTest):

	def setup(self):
		super(TestListGames, self).setup()

		# Put some data into the database

		cat = models.SportCategory(name='Ball games')
		cat.put()

		cat1 = models.SportCategory(name='Basket Ball')
		cat1.add_parent(cat)
		cat1.put()

		cat2 = models.SportCategory(name='Football')
		cat2.add_parent(cat)
		cat2.put()

		user = usermodels.User(full_name="Adrian Letchford")
		user.put()

		msg = messages.NewGame(
			categories = ["Basket Ball"],
			level = 1,
			time = datetime.now(),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		game = actions.create_new_game(user, msg)

	def test(self):
		games = actions.list_games().games

		assert len(games) == 1
		assert games[0].name == "Adrian's big play off"
		assert games[0].categories_full[0].name == "Basket Ball"


