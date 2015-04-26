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

class APITest(HRDatastoreTest):
	def setup(self):

		super(APITest, self).setup()

		# Expose the api
		self.api = modules.sports.api.Sports()

		# Put users in the database
		self.a_user = models.User(full_name = "Dicky Johnson", first_name="Dicky")
		self.a_user.initialise_new_token()
		self.a_user.put()



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

