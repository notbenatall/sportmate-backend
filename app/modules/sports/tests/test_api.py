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

import modules.users.messages as usermessages
import modules.users.models as usermodels
import modules.sports.models as models
import modules.sports.actions as actions
import modules.sports.messages as messages
import modules.sports.api

import modules.misc as misc
import modules.misc.models

class APITest(HRDatastoreTest):
	def setup(self):

		super(APITest, self).setup()

		# Expose the api
		self.api = modules.sports.api.Sports()

		# Put users in the database
		self.a_user = models.User(full_name = "Dicky Johnson", first_name="Dicky")
		self.a_user.initialise_new_token()
		self.a_user.put()

		cat = models.SportCategory(name='American Football')
		cat.put()

class TestGeneral(APITest):

	def test_create_new_game(self):

		send_msg = messages.NewGame(
			token = self.a_user.get_token(),
			categories = ["American Football"],
			level = 1,
			time = datetime.now(),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		game = self.api.create_new_game(send_msg)

		assert game.players_needed == 2
		assert game.lat == 34



class TestJoinGame(APITest):

	def setup(self):
		super(TestJoinGame, self).setup()

		self.tom = usermodels.User(full_name="Tom", first_name="Tom")
		self.tom.initialise_new_token()
		self.tom.put()

		self.user = usermodels.User(full_name="Adrian", first_name="Adrian")
		self.user.initialise_new_token()
		self.user.put()

		cat = models.SportCategory(name='Basket Ball')
		cat.put()

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

		msg = messages.GameIdentifier(
			token=self.tom.get_token(),
			key=self.game.key.urlsafe())

		game_msg = self.api.join_game(msg)


		game_list = models.UserGameList.get_or_create_addable_game_list(self.tom)
		game = self.game.key.get()

		assert game_list.games[0] == self.game.key
		assert game.players[0] == self.user.key
		assert game.players[1] == self.tom.key
		assert game.players_joined == 2



class TestGetUpcoming(APITest):

	def setup(self):
		super(TestGetUpcoming, self).setup()

		self.tom = usermodels.User(full_name="Tom", first_name="Tom")
		self.tom.initialise_new_token()
		self.tom.put()

		self.user = usermodels.User(full_name="Adrian", first_name="Adrian")
		self.user.put()

		self.cat = models.SportCategory(name='Basketball')
		self.cat.put()

		msg = messages.NewGame(
			categories = ["Basketball"],
			level = 1,
			time = datetime.now()+ timedelta(days=7),
			name = "Adrian's big play off",
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		self.game = actions.create_new_game(self.user, msg)

		actions.join_game(self.tom, self.game)

	def test(self):

		msg = usermessages.AuthUser(token=self.tom.get_token())

		games_msg = self.api.get_upcoming(msg)

		assert len(games_msg.games) == 1
		assert games_msg.games[0].name == "Adrian's big play off"


class TestLeaveGame(APITest):

	def setup(self):
		super(TestLeaveGame, self).setup()

		self.tom = usermodels.User(full_name="Tom", first_name="Tom")
		self.tom.initialise_new_token()
		self.tom.put()

		self.user = usermodels.User(full_name="Adrian", first_name="Adrian")
		self.user.put()

		cat = models.SportCategory(name='Basketball')
		cat.put()

		msg = messages.NewGame(
			categories = ["Basketball"],
			time = datetime.now(),
			players_needed = 2,
			lat = 34.0,
			lon = 89.0)

		self.game = actions.create_new_game(self.user, msg)
		actions.join_game(self.tom, self.game)


	def test(self):

		assert self.game.players_joined == 2

		msg = messages.GameIdentifier(token=self.tom.get_token(), key=self.game.key.urlsafe())

		game_msg = self.api.leave_game(msg)

		game_list = models.UserGameList.get_or_create_addable_game_list(self.tom)

		assert self.tom.key.id() not in game_msg.player_ids
		assert game_msg.players_joined == 1


class TestGetAllCategories(DatastoreTest):

	def setup(self):
		super(TestGetAllCategories, self).setup()

		# Expose the api
		self.api = modules.sports.api.Sports()
	
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




class TestSportProfiles(APITest):

	def setup(self):
		super(TestSportProfiles, self).setup()

		self.adrian = usermodels.User(full_name="Adrian", first_name="Adrian")
		self.adrian.initialise_new_token()
		self.adrian.put()

		self.tom = usermodels.User(full_name="Tom", first_name="Tom")
		self.tom.initialise_new_token()
		self.tom.put()

		self.cat = models.SportCategory(name='Basketball')
		self.cat.put()

	def test_get_sport_profiles(self):

		msg = messages.SportProfileRequest(
			token=self.adrian.get_token(),
			user_id=self.adrian.key.id(), 
			sport_category_id="basketball", 
			level=5)

		profile = self.api.add_sport_profile(msg)
		profiles = self.api.list_sport_profiles(msg).profiles

		assert profile.sport.name == "Basketball"
		assert profile.level == 5

		assert profiles[0].sport.name == "Basketball"
		assert profiles[0].level == 5


	def test_modify_sport_profiles(self):

		msg = messages.SportProfileRequest(
			token=self.tom.get_token(),
			user_id=self.tom.key.id(), 
			sport_category_id="basketball", 
			level=5)

		profile = self.api.add_sport_profile(msg)

		msg.level = 0
		profile = self.api.add_sport_profile(msg)

		profiles = self.api.list_sport_profiles(msg).profiles

		assert profile.sport.name == "Basketball"
		assert profile.level == 0

		assert profiles[0].sport.name == "Basketball"
		assert profiles[0].level == 0

	def test_delete_sport_profiles(self):

		msg = messages.SportProfileRequest(
			token=self.adrian.get_token(),
			user_id=self.adrian.key.id(), 
			sport_category_id="basketball", 
			level=5)

		profile = self.api.add_sport_profile(msg)
		self.api.delete_sport_profile(msg)

		profiles = self.api.list_sport_profiles(msg).profiles

		assert profile.sport.name == "Basketball"
		assert profile.level == 5

		assert len(profiles) == 0