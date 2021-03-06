import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime, timedelta
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.ext.db import BadValueError
from testtools import DatastoreTest, HRDatastoreTest

import modules.users.models as usermodels
import modules.sports.models as models
import modules.sports.actions as actions
import modules.sports.messages as messages
import modules.sports.exceptions as exceptions

def test_nothing():
	assert True == True

class TestGetAllCategories(DatastoreTest):
	
	def test(self):

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


class TestGeneral(HRDatastoreTest):


	def test_create_new_game(self):

		user = usermodels.User(full_name="Adrian", first_name="Adrian")
		user.put()

		msg = messages.NewGame(
			categories = ["American Football"],
			level = 1,
			time = datetime.now(),
			name = "Adrian's big play off",
			players_needed = 2,
			location_name = "Some place",
			lat = 34.0,
			lon = 89.0,
			description="Please bring shoes.")

		game = actions.create_new_game(user, msg)

		game = game.key.get()

		assert game.key.parent() == user.key
		assert game.players_needed == 2
		assert game.category[0].id() == "american football"
		assert game.geo.lat == 34
		assert game.geo.lon == 89
		assert game.location_name == "Some place"
		assert game.creator == user.key
		assert len(game.players) == 1
		assert game.players[0] == user.key
		assert game.description == "Please bring shoes."

	def test_create_new_game_minimum(self):

		user = usermodels.User(full_name="Adrian", first_name="Adrian")
		user.put()

		msg = messages.NewGame(
			categories = ["American Football"],
			time = datetime.now(),
			players_needed = 2,
			location_name = "Some place")

		game = actions.create_new_game(user, msg)

		game = game.key.get()

		assert game.key.parent() == user.key
		assert game.players_needed == 2
		assert game.category[0].id() == "american football"
		assert game.location_name == "Some place"
		assert game.creator == user.key
		assert len(game.players) == 1
		assert game.players[0] == user.key



class TestListGames(HRDatastoreTest):

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

		user = usermodels.User(full_name="Adrian Letchford", first_name="Adrian")
		user.put()

		tom = usermodels.User(full_name="Tom", first_name="Tom")
		tom.put()

		msg = messages.NewGame(
			categories = ["Basket Ball"],
			level = 1,
			time = datetime.now() + timedelta(days=5),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		game = actions.create_new_game(user, msg)

		actions.join_game(tom, game)

	def test(self):
		games = actions.list_games().games

		assert len(games) == 1
		assert games[0].name == "Adrian's big play off"
		assert games[0].categories_full[0].name == "Basket Ball"
		assert games[0].players[0].full_name == "Adrian Letchford"
		assert games[0].players[1].full_name == "Tom"



class TestModelToMessageConvert(DatastoreTest):

	def test_sport_category(self):

		cat1 = models.SportCategory(name='Ball')

		cat2 = models.SportCategory(name='Basket Ball')
		cat2.add_parent(cat1)

		cat3 = models.SportCategory(name='Extreme Basket Ball')
		cat3.add_parent(cat2)

		msg = actions.sport_category_to_message(cat3)

		assert msg.name == 'Extreme Basket Ball'
		assert msg.paths[0] == 'ball/basket ball'


	def test_game(self):

		start = datetime.now()
		end = datetime.now()

		user = usermodels.User(full_name="Adrian Letchford", first_name="Adrian")
		user.put()

		game = models.Game(
			time = start,
			end_time = end,
			location_name = "Some location",
			geo=ndb.GeoPt(0, 0),
			creator=user.key,
			players=[user.key],
			key=ndb.Key("Game", 'asdrfag')
			)

		msg = actions.game_model_to_message(game)

		assert msg.time == game.time
		assert msg.end_time == game.end_time
		assert msg.location_name == game.location_name
		assert msg.creator_id == user.key.id()
		assert msg.players[0].full_name == "Adrian Letchford"
		assert msg.player_ids[0] == user.key.id()


class TestJoinGame(HRDatastoreTest):

	def test(self):

		tom = usermodels.User(full_name="Tom", first_name="Tom")
		tom.put()

		user = usermodels.User(full_name="Adrian", first_name="Adrian")
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

		actions.join_game(tom, game)

		game_list = models.UserGameList.get_or_create_addable_game_list(tom)
		game = game.key.get()

		assert game_list.games[0] == game.key
		assert game.players[0] == user.key
		assert game.players[1] == tom.key
		assert game.players_joined == 2
		assert not game.show_in_search


	@raises(exceptions.GameIsFullException)
	def test_join_full_game(self):

		tom = usermodels.User(full_name="Tom", first_name="Tom")
		tom.put()

		user = usermodels.User(full_name="Adrian", first_name="Adrian")
		user.put()

		msg = messages.NewGame(
			categories = ["Basket Ball"],
			level = 1,
			time = datetime.now(),
			name = "Adrian's big play off",
			players_needed = 1,
			lat = 34.0,
			lon = 89.0)

		game = actions.create_new_game(user, msg)

		actions.join_game(tom, game)



class TestGetUpcoming(HRDatastoreTest):

	def setup(self):
		super(TestGetUpcoming, self).setup()

		self.tom = usermodels.User(full_name="Tom", first_name="Tom")
		self.tom.put()

		self.user = usermodels.User(full_name="Adrian", first_name="Adrian")
		self.user.put()

		self.cat = models.SportCategory(name='Basketball')
		self.cat.put()

		msg = messages.NewGame(
			categories = ["Basketball"],
			level = 1,
			time = datetime.now() + timedelta(days=7),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		self.game = actions.create_new_game(self.user, msg)

		actions.join_game(self.tom, self.game)

	def test(self):

		games_msg = actions.get_upcoming(self.tom)

		assert len(games_msg.games) == 1
		assert games_msg.games[0].name == "Adrian's big play off"




class TestLeaveGame(HRDatastoreTest):

	def setup(self):
		super(TestLeaveGame, self).setup()

		self.tom = usermodels.User(full_name="Tom", first_name="Tom")
		self.tom.put()

		self.user = usermodels.User(full_name="Adrian", first_name="Adrian")
		self.user.put()

		msg = messages.NewGame(
			categories = ["Basket Ball"],
			level = 1,
			time = datetime.now(),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		self.game = actions.create_new_game(self.user, msg)

		actions.join_game(self.tom, self.game)


	def test(self):

		assert self.game.players_joined == 2

		game = actions.leave_game(self.tom, self.game.key)

		users_game_list = models.UserGameList.get_or_create_addable_game_list(self.tom)
		
		assert self.tom.key not in game.players
		assert game.players_joined == 1
		assert self.game.key not in users_game_list.games


class TestLeaveGameEmpty(HRDatastoreTest):

	def setup(self):
		super(TestLeaveGameEmpty, self).setup()

		self.user = usermodels.User(full_name="Adrian", first_name="Adrian")
		self.user.put()

		msg = messages.NewGame(
			categories = ["Basket Ball"],
			level = 1,
			time = datetime.now(),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		self.game = actions.create_new_game(self.user, msg)

	def test(self):

		game = actions.leave_game(self.user, self.game.key)

		retrieved_game = self.game.key.get()

		assert retrieved_game is None


class TestGetUpcomingOldGames(HRDatastoreTest):

	def setup(self):
		super(TestGetUpcomingOldGames, self).setup()

		self.user = usermodels.User(full_name="Adrian", first_name="Adrian")
		self.user.put()

		self.cat = models.SportCategory(name='Basketball')
		self.cat.put()

		msg = messages.NewGame(
			categories = ["Basketball"],
			level = 1,
			time = datetime.now() - timedelta(days=2),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		self.game = actions.create_new_game(self.user, msg)

	def test(self):

		games_msg = actions.get_upcoming(self.user)

		assert len(games_msg.games) == 0


class TestSportProfiles(DatastoreTest):

	def test_sport_profile_to_message(self):

		cat = models.SportCategory(name='Basketball')
		cat.put()

		profile = models.SportProfile(sport=cat.key, level=0)
		msg = actions.sports_profile_to_message(profile)

		assert msg.sport.name == "Basketball"


	def test_get_sport_profiles(self):

		user = usermodels.User(full_name="Adrian", first_name="Adrian")
		user.put()

		cat = models.SportCategory(name='Basketball')
		cat.put()

		msg = messages.SportProfileRequest(sport_category_id = cat.key.id())

		actions.add_sport_profile(user, msg)

		profiles = actions.get_user_sport_profiles(user).profiles

		assert profiles[0].sport.name == "Basketball"
		assert profiles[0].level == 0


	def test_delete_sport_profiles(self):

		user = usermodels.User(full_name="Bob", first_name="Bob")
		user.put()

		cat = models.SportCategory(name='Football')
		cat.put()

		msg = messages.SportProfileRequest(sport_category_id = cat.key.id())

		actions.add_sport_profile(user, msg)
		actions.delete_sport_profile(user, msg)

		profiles = actions.get_user_sport_profiles(user).profiles

		assert len(profiles) == 0
		

class TestGameComments(HRDatastoreTest):

	def setup(self):
		super(TestGameComments, self).setup()

		self.user = usermodels.User(full_name="Adrian", first_name="Adrian")
		self.user.put()

		self.cat = models.SportCategory(name='Basketball')
		self.cat.put()

		msg = messages.NewGame(
			categories = ["Basketball"],
			level = 1,
			time = datetime.now() - timedelta(days=2),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		self.game = actions.create_new_game(self.user, msg)

	def test_add_comment(self):

		comment = actions.add_comment_to_game(self.user, self.game.key.urlsafe(), "hai!")

		assert comment.user.first_name == "Adrian"
		assert comment.body == "hai!"


	def test_get_latest_comments(self):

		comment = actions.add_comment_to_game(self.user, self.game.key.urlsafe(), "Hello.")

		comments = actions.get_latest_game_comments(self.game.key.urlsafe()).comments

		assert comments[0].body == "Hello."
		assert type(comments[0].created) is datetime





class TestSportmateSearch(DatastoreTest):

	def test(self):

		user = usermodels.User(full_name="Adrian", first_name="Adrian")
		user.put()

		cat = models.SportCategory(name='Basketball')
		cat.put()

		msg = messages.SportProfileRequest(sport_category_id = cat.key.id())

		actions.add_sport_profile(user, msg)


		request = messages.SportmateSearchRequest()
		request.sport_category_id = 'basketball'

		result = actions.search_for_sportmates(request).profiles

		assert result[0].sport.name == "Basketball"
		assert result[0].user.full_name == "Adrian"
