"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds all the actions for the backend system. The system runs on
Google App Engine using the NoSQL DataStore for scalability.
"""

from google.appengine.ext import ndb
from endpoints import NotFoundException
from google.appengine.ext.db import BadValueError
import modules.sports.models as models
import modules.sports.messages as messages
import modules.sports.exceptions as exceptions
from modules.misc.models import get_model
from modules.users.models import User
import mmglue

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def sport_category_to_message(category):
	"""Convert a sport category model into a message."""
	msg = mmglue.message_from_model(category, messages.SportCategory)
	msg.paths = category.paths
	return msg

def game_model_to_message(game):
	"""Convert a game model into a message."""
	msg = mmglue.message_from_model(game, messages.Game)
	msg.lat = game.geo.lat
	msg.lon = game.geo.lon

	categories = [cat_key.get() for cat_key in game.category]

	msg.categories_full = [sport_category_to_message(category)
			for category in categories]

	return msg

def get_all_categories():
	"""Returns a list of all sports categories."""

	categories = models.SportCategory.get_all()

	everything = messages.CategoryList()

	for cat in categories:
		cat_msg = mmglue.message_from_model(cat, messages.SportCategory)
		cat_msg.parent_ids = [parent_key.id() for parent_key in cat.parents]
		everything.categories.append(cat_msg)

	return everything

def create_new_game(auth_user, details):
	"""Creates a new sport game."""

	if type(details) is not messages.NewGame:
		raise NotFoundException("Can only create a game with a NewGame message.")

	if not hasattr(auth_user, 'key') or auth_user.key.kind() != 'User':
		raise NotFoundException("I require a user to create a game.")

	category_keys = [models.SportCategory.key_from_name(cat)
		for cat in details.categories]

	game = mmglue.model_from_message(details, models.Game,
		parent=auth_user.key,
		category=category_keys,
		players_full=False,
		players_joined=1,
		geo=ndb.GeoPt(details.lat, details.lon))

	game.put()

	return game

def list_games():
	"""Return a list of all the games."""
	query = models.Game.query()
	games = query.fetch()

	# Turn into messages
	games_msg = messages.GameList()
	games_msg.games = [game_model_to_message(game) for game in games]

	return games_msg

@ndb.transactional(xg=True)
def join_game(user, game):

	user = get_model(user, User)
	game = get_model(game, models.Game)

	if game.players_full:
		raise exceptions.GameIsFullException()

	# Add user to the game
	game.players.append(user.key)
	game.players_joined += 1

	# Add game to the user
	game_list = models.UserGameList.get_or_create_addable_game_list(user)
	game_list.add_game(game.key)

	game.put()
	game_list.put()


# Modify a game

# Join a game

# List games (with filters)

# Add sport profile

# Get sport profile(s) of a user

# Get games made by a user