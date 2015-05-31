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
from modules.misc.messages import VoidMessage

import modules.api

@modules.api.API.api_class(resource_name='sports')
class Sports(remote.Service):
	"""
	Access and Modify information about sports.

	The decorator parameter "resource_name='sports'" does not go into the REST
	path!
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



	@endpoints.method(AuthUser, messages.CategoryList, path='categories/all',
		http_method='POST', name='allcategories')
	def get_all_categories(self, request):
		"""Returns a list of all the user's upcoming games."""
		verify_and_get_user(token=request.token)
		return actions.get_all_categories()


	@endpoints.method(messages.SportProfileRequest, messages.SportProfileList, path='sport/profile',
		http_method='POST', name='listprofiles')
	def list_sport_profiles(self, request):
		"""Returns a list of all the user's sports profiles."""

		user_id = request.user_id
		profiles = actions.get_user_sport_profiles(user_id)
		return profiles


	@endpoints.method(messages.SportProfileRequest, messages.SportProfile, path='sport/profile',
		http_method='PUT', name='addprofile')
	def add_sport_profile(self, request):
		"""Adds a sport profile to the authenticating user."""

		auth_user = verify_and_get_user(token=request.token)

		profile = actions.add_sport_profile(auth_user, request)

		return profile


	@endpoints.method(messages.SportProfileRequest, VoidMessage, path='sport/profile',
		http_method='DELETE', name='removeprofile')
	def delete_sport_profile(self, request):
		"""Delets a sport profile from the authenticating user."""

		auth_user = verify_and_get_user(token=request.token)

		actions.delete_sport_profile(auth_user, request)

		return VoidMessage()


	@endpoints.method(messages.AddGameComment, messages.GameComment, path='game/comment',
		http_method='PUT', name='addcomment')
	def add_game_comment(self, request):
		"""Adds a comment to a game."""

		auth_user = verify_and_get_user(token=request.token)

		comment = actions.add_comment_to_game(auth_user, request.game_key, request.text)

		print comment
		
		return comment


	@endpoints.method(messages.GameRequest, messages.GameCommentThread, path='game/comment',
		http_method='GET', name='getgamecomments')
	def get_game_comments(self, request):
		"""Gets the latest comments on a game."""

		comments = actions.get_latest_game_comments(request.game_key)

		return comments