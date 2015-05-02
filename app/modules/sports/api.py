"""
Sportmate API

Module: sports.api

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Holds the endpoints for the sports module.
"""
# pylint: disable=no-self-use, no-init, unused-argument

from google.appengine.ext import ndb
import endpoints
from protorpc import remote

from modules.users.messages import AuthUser
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

		return actions.game_model_to_message(game)


	@endpoints.method(messages.GamesRequest, messages.GameList, path='games',
		http_method='GET', name='listgames')
	def list_games(self, request):
		"""Returns a list of all the games."""
		games_msg = actions.list_games()
		return games_msg


	@endpoints.method(messages.GameIdentifier, messages.Game, path='game/join',
		http_method='POST', name='joingame')
	def join_game(self, request):
		"""The authenticating user joins a game."""
		auth_user = verify_and_get_user(token=request.token)

		game = actions.join_game(auth_user, ndb.Key(urlsafe=request.key))

		return actions.game_model_to_message(game)


	@endpoints.method(messages.GameIdentifier, messages.Game, path='game/leave',
		http_method='POST', name='leavegame')
	def leave_game(self, request):
		"""The authenticating user leaves a game."""
		auth_user = verify_and_get_user(token=request.token)

		game = actions.leave_game(auth_user, ndb.Key(urlsafe=request.key))

		return actions.game_model_to_message(game)


	@endpoints.method(AuthUser, messages.GameList, path='games/upcoming',
		http_method='POST', name='gamesupcoming')
	def get_upcoming(self, request):
		"""Returns a list of all the user's upcoming games."""
		auth_user = verify_and_get_user(token=request.token)
		return actions.get_upcoming(auth_user)