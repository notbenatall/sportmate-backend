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

		msg = messages.JoinGame(
			token=self.tom.get_token(),
			key=self.game.key.urlsafe())

		game_msg = self.api.join_game(msg)


		game_list = models.UserGameList.get_or_create_addable_game_list(self.tom)
		game = self.game.key.get()

		assert game_list.games[0] == self.game.key
		assert game.players[0] == self.user.key
		assert game.players[1] == self.tom.key
		assert game.players_joined == 2
