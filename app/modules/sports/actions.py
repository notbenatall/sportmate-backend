"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds all the actions for the sports module.
"""

from google.appengine.ext import ndb
from endpoints import NotFoundException
import modules.sports.models as models
import modules.sports.messages as messages
import modules.sports.exceptions as exceptions
from modules.misc.models import get_model
from modules.users.models import User
from modules.users.actions import user_to_message
import mmglue
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def sport_category_to_message(category):
	"""Convert a sport category model into a message."""
	msg = mmglue.message_from_model(category, messages.SportCategory)
	msg.paths = category.paths
	msg.parent_ids = [c.id() for c in category.parents]
	return msg

def game_model_to_message(game):
	"""Convert a game model into a message."""
	msg = mmglue.message_from_model(game, messages.Game)

	msg.key = game.key.urlsafe()

	if game.geo:
		msg.lat = game.geo.lat
		msg.lon = game.geo.lon

	categories = ndb.get_multi(game.category)
	msg.categories_full = [sport_category_to_message(category)
			for category in categories]

	list_of_players = ndb.get_multi(game.players[:5])
	msg.players = [user_to_message(player) for player in list_of_players]

	msg.player_ids = [player.id() for player in game.players]

	return msg


def list_of_games_to_message(games):
	"""Converts a list of games into a message."""
	msg = messages.GameList()
	msg.games = [game_model_to_message(game) for game in games]
	return msg


def sports_profile_to_message(profile):
	"""Convert a sport profile to a message."""
	msg = messages.SportProfile()
	msg.level = profile.level
	msg.sport = sport_category_to_message(profile.sport.get())
	return msg


def game_comment_to_message(comment):
	"""Convert a game comment to a message."""
	msg = messages.GameComment()
	msg.body = comment.body
	msg.user = user_to_message(comment.user.get())
	msg.created = comment.created
	return msg


def get_all_categories():
	"""Returns a list of all sports categories."""

	categories = models.SportCategory.get_all()

	everything = messages.CategoryList()

	everything.categories = [sport_category_to_message(c) for c in categories]

	return everything

@ndb.transactional(xg=True)
def create_new_game(auth_user, details):
	"""Creates a new sport game."""

	if type(details) is not messages.NewGame:
		raise NotFoundException("Can only create a game with a NewGame message.")

	if not hasattr(auth_user, 'key') or auth_user.key.kind() != 'User':
		raise NotFoundException("I require a user to create a game.")

	category_keys = [models.SportCategory.key_from_name(cat)
		for cat in details.categories]

	# Make sure the dates are in UTC time
	if details.time.tzinfo is not None and details.time.utcoffset() is not None:
		details.time = details.time.replace(tzinfo=None) - details.time.utcoffset()

	game = mmglue.model_from_message(details, models.Game,
		parent=auth_user.key,
		category=category_keys,
		players_full=False,
		players_joined=1,
		players=[auth_user.key])

	if details.lat and details.lon:
		game.geo = ndb.GeoPt(details.lat, details.lon)

	game.put()

	# Add game to the user
	game_list = models.UserGameList.get_or_create_addable_game_list(auth_user)
	game_list.add_game(game.key)

	game_list.put()

	return game

def list_games():
	"""Return a list of all the games."""
	query = models.Game.query(models.Game.time > datetime.now())
	games = query.fetch()
	games.sort(key=lambda g: g.time)
	return list_of_games_to_message(games)

@ndb.transactional(xg=True)
def join_game(user, game):
	"""Adds a user to a game."""
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

	return game

@ndb.transactional(xg=True)
def leave_game(user, game):
	"""
	Remove a user from a game.

	TODO: Need to manage the situation of multiple user game lists.
	"""

	user = get_model(user, User)
	game = get_model(game, models.Game)

	users_game_list = models.UserGameList.get_or_create_addable_game_list(user)

	# Check to make sure that the user is in the game
	if user.key not in game.players:
		raise NotFoundException

	# Check to make sure that the game is found with the user
	if game.key not in users_game_list.games:
		raise NotFoundException

	# Remove user from the game
	game.players.remove(user.key)
	game.players_joined -= 1

	# Remove game from the user
	users_game_list.remove_game(game.key)

	if len(game.players) == 0:
		game.key.delete()
	else:
		game.put()

	users_game_list.put()

	return game


def get_upcoming(auth_user):
	"""Gets the upcoming games that a user is attending."""
	user = get_model(auth_user, User)

	game_list = models.UserGameList.get_or_create_addable_game_list(user)
	games = ndb.get_multi(game_list.games)

	upcoming_games = [g for g in games if g.time > datetime.now()]
	upcoming_games.sort(key=lambda g: g.time)

	return list_of_games_to_message(upcoming_games)


def get_user_sport_profiles(user):
	"""
	Returns a list of all a user's profiles.
	"""

	user = get_model(user, User)

	query = models.SportProfile.query(ancestor=user.key)
	profiles = query.fetch()

	msg = messages.SportProfileList()
	msg.profiles = [sports_profile_to_message(p) for p in profiles]

	return msg


def add_sport_profile(auth_user, msg):
	"""
	Creates a new sport profile.

	Param:
		msg - messages.SportProfileRequest
	"""

	user = get_model(auth_user, User)

	sport = models.SportCategory.get_by_name(msg.sport_category_id)

	profile = models.SportProfile(
		parent=user.key,
		sport=sport.key,
		level=msg.level)

	profile.put()

	return sports_profile_to_message(profile)


def delete_sport_profile(auth_user, msg):
	"""
	Delete a sport profile.

	Param:
		msg - messages.SportProfileRequest
	"""

	user = get_model(auth_user, User)
	profile_key = models.SportProfile.make_key(user.key,
		msg.sport_category_id)

	profile_key.delete()


def add_comment_to_game(user, game_key, text):
	"""
	Adds a comment to a game written.
	"""

	user = get_model(user, User)
	game = ndb.Key(urlsafe=game_key).get()

	comment = models.GameComment(user=user.key, body=text)

	
	number = models.GameCommentThread.get_thread_number(game.key)

	if number is None:
		new_key = models.GameCommentThread.make_key(game.key, 1)
		thread = models.GameCommentThread(key=new_key)
	else:
		thread = models.GameCommentThread.get_by_key(game.key, number)

	# If this thread is full, create another one
	if thread.is_full():
		new_key = models.GameCommentThread.make_key(game.key, thread.key.id()+1) #pylint: disable=maybe-no-member
		thread = Thread(key=new_key)

	thread.comments.append(comment)
	thread.put()  #pylint: disable=maybe-no-member

	return game_comment_to_message(comment)


def get_latest_game_comments(game_key):
	"""
	Returns a list of the latest comments on a game.
	"""
	game = ndb.Key(urlsafe=game_key).get()

	number = models.GameCommentThread.get_thread_number(game.key)

	if number is None:
		return messages.GameCommentThread()

	thread = models.GameCommentThread.get_by_key(game.key, number)

	msg = messages.GameCommentThread()
	msg.comments = [game_comment_to_message(comment) for comment in thread.comments]

	return msg



# Modify a game

# Get games made by a user