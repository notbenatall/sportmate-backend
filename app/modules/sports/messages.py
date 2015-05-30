"""
Sportmate API

Module: sports

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable=invalid-name,too-few-public-methods

from protorpc import messages
from protorpc import message_types

from modules.users.messages import User


class SportCategory(messages.Message):
	"""Message containing a sports category."""
	name = messages.StringField(1)
	id = messages.StringField(2)
	parent_ids = messages.StringField(3, repeated=True)
	paths = messages.StringField(4, repeated=True)

class CategoryList(messages.Message):
	"""Message containing a list of categories."""
	categories = messages.MessageField(SportCategory, 1, repeated=True)

class Game(messages.Message):
	"""Message containing a game."""
	categories = messages.StringField(1, repeated=True)
	players_full = messages.BooleanField(2, required=True)
	level = messages.IntegerField(3, required=True)
	time = message_types.DateTimeField(4, required=True)
	name = messages.StringField(5, required=False)
	players_needed = messages.IntegerField(6, required=True)
	players_joined = messages.IntegerField(7, required=True)
	lat = messages.FloatField(8, required=False)
	lon = messages.FloatField(9, required=False)
	categories_full = messages.MessageField(SportCategory, 10, repeated=True)
	end_time = message_types.DateTimeField(11, required=False)
	location_name = messages.StringField(12, required=False)
	creator_id = messages.IntegerField(13, required=True)
	players = messages.MessageField(User, 14, repeated=True)
	key = messages.StringField(15)
	player_ids = messages.IntegerField(16, repeated=True)

class NewGame(messages.Message):
	"""Message containing a brand new game to add to the system."""
	categories = messages.StringField(1, repeated=True)
	level = messages.IntegerField(2, required=False)
	time = message_types.DateTimeField(3, required=True)
	name = messages.StringField(4, required=False)
	players_needed = messages.IntegerField(5, required=True)
	lat = messages.FloatField(6, required=False)
	lon = messages.FloatField(7, required=False)

	token = messages.StringField(8, required=True)

	end_time = message_types.DateTimeField(9, required=False)
	location_name = messages.StringField(10, required=False)


class GameList(messages.Message):
	"""Message containing a list of games."""
	games = messages.MessageField(Game, 1, repeated=True)

class GameRequest(messages.Message):
	"""A request for information about a specific game."""
	game_key = messages.StringField(1, required=True)

class GamesRequest(messages.Message):
	"""Message containing a request for a list of games."""
	pass

class GameIdentifier(messages.Message):
	"""Message containing a request to join a game."""
	token = messages.StringField(1, required=True)
	# The game's key
	key = messages.StringField(2, required=True)

class SportProfile(messages.Message):
	"""
	Message for a sports profile.
	"""
	sport = messages.MessageField(SportCategory, 1, required=True)
	level = messages.IntegerField(2, required=True)


class SportProfileList(messages.Message):
	"""
	List of sport profiles.
	"""
	profiles = messages.MessageField(SportProfile, 1, repeated=True)



class SportProfileRequest(messages.Message):
	"""
	Message for an action on a sport profile
	"""
	token = messages.StringField(1, required=False)
	user_id = messages.IntegerField(2, required=False)
	
	sport_category_id = messages.StringField(3, required=False)
	level = messages.IntegerField(4, required=False, default=0)


class AddGameComment(messages.Message):
	"""
	Message for an authenticating user to add a game comment.
	"""
	token = messages.StringField(1, required=True)
	game_key = messages.StringField(2, required=True)
	text = messages.StringField(3, required=True)

class GameComment(messages.Message):
	"""
	Message containing a game comment
	"""

	body = messages.StringField(1, required=True)
	user = messages.MessageField(User, 2, required=True)
	created = message_types.DateTimeField(3, required=True)


class GameCommentThread(messages.Message):
	"""
	A page of comments on a game.
	"""
	comments = messages.MessageField(GameComment, 1, repeated=True)