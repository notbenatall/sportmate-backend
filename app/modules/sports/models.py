"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds all the models.
"""
# pylint: disable=too-few-public-methods

from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from modules.misc import validate_parent
from modules.users.models import User
import Geohash


class SportCategory(ndb.Model):
	"""Models a sports category."""

	name = ndb.StringProperty(indexed=False, required=True)

	# These properties are internally managed and do not need to be set outside
	# of this class.
	paths = ndb.StringProperty(indexed=True, repeated=True)
	parents = ndb.KeyProperty(indexed=False, repeated=True)

	def __init__(self, **kwargs):

		if 'key' in kwargs:
			raise BadValueError

		super(SportCategory, self).__init__(**kwargs)

		if 'name' in kwargs:
			self.key = self.key_from_name(self.name)

	def add_parent(self, parent):
		"""
		Adds a parent to the sport category and ensures that it is a
		SportCategory.
		"""

		if type(parent) is not SportCategory:
			raise BadValueError

		if len(parent.key.pairs()) != 1:
			raise BadValueError

		parent_id = parent.key.id()

		# Add parent's paths to self's paths
		if parent.paths is None or len(parent.paths) == 0:
			self.paths.append(parent_id)
		else:
			for path in parent.paths:
				new_path = path.strip("/") + "/" + parent_id

				if new_path in self.paths:
					continue

				self.paths.append(new_path)

		self.parents.append(parent.key)

	@staticmethod
	def get_by_name(name):
		"""Returns a sport category by its name."""
		key = ndb.Key(SportCategory, name.lower())
		cat = key.get()
		return cat

	@staticmethod
	def get_all():
		"""Return a list of all categories."""
		query = SportCategory.query()
		categories = query.fetch()
		return categories

	@staticmethod
	def key_from_name(name):
		"""Turns a sport name into a key associated with its object."""
		return ndb.Key(SportCategory, name.lower())



class Game(ndb.Model):
	"""
	Parent: User
	"""

	category = ndb.KeyProperty(kind=SportCategory, repeated=True, indexed=True)
	players_full = ndb.BooleanProperty(indexed=False, default=False)
	level = ndb.IntegerProperty(indexed=True, default=0)
	time = ndb.DateTimeProperty(indexed=True, required=True)
	end_time = ndb.DateTimeProperty(indexed=False, required=False)
	name = ndb.StringProperty(indexed=False, required=False)
	players_needed = ndb.IntegerProperty(indexed=False, required=True)
	players_joined = ndb.IntegerProperty(indexed=False, default=1, required=True)
	geo = ndb.GeoPtProperty(indexed=False, required=False)
	geohash = ndb.StringProperty(indexed=True, required=False)
	location_name = ndb.StringProperty(indexed=False)
	players = ndb.KeyProperty(kind=User, indexed=False, repeated=True)
	creator = ndb.KeyProperty(kind=User, required=True)
	show_in_search = ndb.BooleanProperty(indexed=True, default=True)
	description = ndb.StringProperty(indexed=False, required=False)


	def update_geohash(self):
		"""
		Sets the geohash to correspond to the coordinates stored in self.geo.
		"""
		if self.geo:
			self.geohash = Geohash.encode(self.geo.lat, self.geo.lon, precision=20)

	def validate(self):
		"""Validates this model."""
		validate_parent(self, User)

		# The game model must have either a geo location or a location name
		if not self.geo and not self.location_name:
			raise BadValueError

		self.creator = self.key.parent()

		if self.category is None or len(self.category) == 0:
			raise BadValueError

		self.update_geohash()

		if self.players_joined > self.players_needed:
			raise BadValueError

		self.players_full = self.players_joined == self.players_needed

		self.show_in_search = not self.players_full

	def put(self):
		"""Write this model to the database after validating."""
		self.validate()
		super(Game, self).put()


class SportProfile(ndb.Model):
	"""
	Holds a users's information concerning a particular sport.

	Parent: User
	"""
	sport = ndb.KeyProperty(kind=SportCategory, indexed=True, required=True)
	level = ndb.IntegerProperty(indexed=True, default=0)


	def __init__(self, **kwargs):
		"""
		Make the model. Defines the key structure.
		"""

		if 'key' in kwargs:
			raise BadValueError

		super(SportProfile, self).__init__(**kwargs)

		# Create the key
		if 'parent' in kwargs:
			self.key = self.make_key(kwargs['parent'], self.sport.id())


	@staticmethod
	def get_unique(user_key, sport_category_id):
		"""Returns a profile from the user and it's name."""
		key = SportProfile.make_key(user_key, sport_category_id)
		return key.get()

	@staticmethod
	def make_key(user_key, sport_category_id):
		"""Makes a key."""
		user_pairs = list(user_key.pairs())
		pairs = user_pairs + [(SportProfile, sport_category_id)]
		return ndb.Key(pairs=pairs)


class UserGameList(ndb.Model):
	"""
	Holds a users's games.

	Parent: User
	"""
	games = ndb.KeyProperty(kind=Game, indexed=False, repeated=True)
	full = ndb.BooleanProperty(indexed=True, default=False)

	def validate(self):
		"""Validates this model."""
		validate_parent(self, User)

		if len(self.games) > 5000:
			raise BadValueError

	def _set_full(self):
		"""Set the full property."""
		if len(self.games) == 5000:
			self.full = True
		else:
			self.full = False

	def put(self):
		"""Write this model to the database after validating."""
		self.validate()
		super(UserGameList, self).put()

	def add_game(self, game):
		"""Add a game to this games list."""
		if len(self.games) >= 5000:
			raise Exception("Full.")

		self.games.append(game)

		self._set_full()

	def remove_game(self, game):
		"""Removes a game from this list."""
		self.games.remove(game)
		self._set_full()


	@staticmethod
	def get_or_create_addable_game_list(user):
		"""
		Given a user, returns a games list that can have at least one more
		game added to it.
		"""
		query = UserGameList.query(ancestor=user.key)
		query.filter(UserGameList.full == False)
		game_list = query.get()

		if game_list is None:
			game_list = UserGameList(parent=user.key)

		return game_list


class GameComment(ndb.Model):
	"""
	Comment on a game.

	This model should not be in the datastore as a seperate entity. This is
	designed to be a nested model inside GameCommentThread.
	"""

	body = ndb.StringProperty(indexed=False)
	user = ndb.KeyProperty(kind=User, indexed=False, required=True)
	created = ndb.DateTimeProperty(indexed=False, required=True, auto_now_add=True)


class GameCommentThread(ndb.Model):
	"""
	A thread of comments on a game.

	Parent: Game
	Key: [Game Key, (GameCommentThread, number)]
	"""
	comments = ndb.StructuredProperty(GameComment, repeated=True)


	def is_full(self):
		"""Determines if the thread is full."""
		return len(self.comments) >= 5000

	@staticmethod
	def get_thread_number(game_key):
		"""
		Returns the latest thread page of a game.
		"""

		thread_keys = GameCommentThread.query(ancestor=game_key).fetch(keys_only=True)
		if len(thread_keys) == 0:
			return None

		thread_ids = [key.id() for key in thread_keys]
		thread_ids.sort()

		return thread_ids[-1]


	@staticmethod
	def make_key(game_key, number):
		"""
		Makes a key.
		"""
		pairs = list(game_key.pairs())
		pairs.append((GameCommentThread, number))
		return ndb.Key(pairs=pairs)


	@staticmethod
	def get_by_key(game_key, number):
		"""Returns the thread for the given parent and number."""
		pairs = list(game_key.pairs()) + [(GameCommentThread, number)]
		key = ndb.Key(pairs=pairs)
		thread = key.get()
		return thread