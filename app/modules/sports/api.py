"""
Sportmate API

Module: sports.api

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Holds the endpoints for the sports module.
"""
# pylint: disable=no-self-use, no-init, unused-argument

import endpoints
from protorpc import remote
import mmglue

from modules.users.actions import verify_and_get_user
import modules.sports.actions as actions
import modules.sports.messages as messages

import modules.api

@modules.api.API.api_class(resource_name='sports')
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


	@endpoints.method(messages.GamesRequest, messages.GameList, path='games',
		http_method='GET', name='listgames')
	def list_games(self, request):
		"""Returns a list of all the games."""
		games_msg = actions.list_games()
		return games_msg