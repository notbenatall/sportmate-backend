"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds all the actions for the backend system. The system runs on
Google App Engine using the NoSQL DataStore for scalability.
"""

from google.appengine.ext import ndb
from endpoints import NotFoundException
import modules.sports.models as models
import modules.sports.messages as messages
import mmglue

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

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

	game = models.Game(
		parent=auth_user.key,
		category=category_keys,
		players_full=False,
		level=details.level,
		time=details.time,
		name=details.name,
		players_needed=details.players_needed,
		players_joined=1,
		geo=ndb.GeoPt(details.lat, details.lon))

	game.put()

	return game


# Modify a game

# Join a game

# List games (with filters)

# Add sport profile

# Get sport profile(s) of a user

# Get games made by a user