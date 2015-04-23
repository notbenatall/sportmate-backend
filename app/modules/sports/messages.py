"""
Sportmate API

Module: sports

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable=invalid-name,too-few-public-methods

from protorpc import messages
from protorpc import message_types


class SportCategory(messages.Message):
	"""Message containing a sports category."""
	name = messages.StringField(1)
	id = messages.StringField(2)
	parent_ids = messages.StringField(3, repeated=True)

class CategoryList(messages.Message):
	"""Message containing a list of categories."""
	categories = messages.MessageField(SportCategory, 1, repeated=True)

class Game(messages.Message):
	"""Message containing a game."""
	categories = messages.StringField(1, repeated=True)
	players_full = messages.BooleanField(2, required=True)
	level = messages.IntegerField(3, required=True)
	time = message_types.DateTimeField(4, required=True)
	name = messages.StringField(5, required=True)
	players_needed = messages.IntegerField(6, required=True)
	players_joined = messages.IntegerField(7, required=True)
	lat = messages.FloatField(8, required=True)
	lon = messages.FloatField(9, required=True)
	categories_full = messages.MessageField(SportCategory, 10, repeated=True)

class NewGame(messages.Message):
	"""Message containing a brand new game to add to the system."""
	categories = messages.StringField(1, repeated=True)
	level = messages.IntegerField(2, required=True)
	time = message_types.DateTimeField(3, required=True)
	name = messages.StringField(4, required=True)
	players_needed = messages.IntegerField(5, required=True)
	lat = messages.FloatField(6, required=True)
	lon = messages.FloatField(7, required=True)

	token = messages.StringField(8, required=True)


class GameList(messages.Message):
	"""Message containing a list of games."""
	games = messages.MessageField(Game, 1, repeated=True)


class GamesRequest(messages.Message):
	"""Message containing a request for a list of games."""
	pass