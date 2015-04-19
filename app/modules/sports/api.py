"""
Sportmate API

Module: sports.api

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Holds the endpoints for the sports module.
"""
# pylint: disable=no-self-use, no-init

import endpoints
from protorpc import remote
import mmglue

from modules.users.actions import verify_and_get_user
import modules.sports.actions as actions
import modules.sports.messages as messages

# Package name
API = endpoints.api(name='sports', version='v1.0')

@API.api_class(resource_name='sports')
class Sports(remote.Service):
	"""
	Access and Modify information about sports.
	"""

	@endpoints.method(messages.NewGame, messages.Game, path='create',
		http_method='POST', name='creategame')
	def create_new_game(self, request):
		"""Adds a new game to the system."""

		auth_user = verify_and_get_user(token=request.token)

		game = actions.create_new_game(auth_user, request)

		msg = mmglue.message_from_model(game, messages.Game)
		msg.lat = game.geo.lat
		msg.lon = game.geo.lon

		return msg