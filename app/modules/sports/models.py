"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds all the models.
"""
# pylint: disable=too-few-public-methods

from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from misc import validate_parent
from users.models import User
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
	players_full = ndb.BooleanProperty(indexed=True, default=False)
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


	def update_geohash(self):
		"""
		Sets the geohash to correspond to the coordinates stored in self.geo.
		"""
		if self.geo:
			self.geohash = Geohash.encode(self.geo.lat, self.geo.lon, precision=20)

	def validate(self):
		"""Validates this model."""
		validate_parent(self, User)

		self.creator = self.key.parent()

		if self.category is None or len(self.category) == 0:
			raise BadValueError

		self.update_geohash()

		if self.players_joined > self.players_needed:
			raise BadValueError

		self.players_full = self.players_joined == self.players_needed

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

	def put(self):
		"""Write this model to the database after validating."""
		self.validate()
		super(UserGameList, self).put()

	def add_game(self, game):
		"""Add a game to this games list."""
		if len(self.games) >= 5000:
			raise Exception("Full.")

		self.games.append(game)

		if len(self.games) == 5000:
			self.full = True
		else:
			self.full = False

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