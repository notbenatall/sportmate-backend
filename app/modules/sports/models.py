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
	paths = ndb.KeyProperty(indexed=True, repeated=True)
	parents = ndb.KeyProperty(indexed=False, repeated=True)

	def __init__(self, **kwargs):

		if 'key' in kwargs:
			raise BadValueError

		super(SportCategory, self).__init__(**kwargs)

		if 'name' in kwargs:
			key = ndb.Key(SportCategory, self.name.lower())
			self.key = key

	def add_parent(self, parent):
		"""
		Adds a parent to the sport category and ensures that it is a
		SportCategory.
		"""

		if type(parent) is not SportCategory:
			raise BadValueError

		if len(parent.key.pairs()) != 1:
			raise BadValueError

		parent_pair = parent.key.pairs()[0]

		# Add parent's paths to self's paths
		if parent.paths is None or len(parent.paths) == 0:
			self.paths.append(ndb.Key(pairs=[parent_pair]))
		else:
			for path in parent.paths:
				new_path = list(path.pairs())
				new_path.append(parent_pair)
				new_path_key = ndb.Key(pairs=new_path)

				if new_path_key in self.paths:
					continue

				self.paths.append(new_path_key)

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



class Game(ndb.Model):
	"""
	Parent: User
	"""

	category = ndb.KeyProperty(kind=SportCategory, repeated=True, indexed=True)
	players_full = ndb.BooleanProperty(indexed=True, default=False)
	level = ndb.IntegerProperty(indexed=True, default=0)
	time = ndb.DateTimeProperty(indexed=True, required=True)
	name = ndb.StringProperty(indexed=False, required=True)
	players_needed = ndb.IntegerProperty(indexed=False, required=True)
	players_joined = ndb.IntegerProperty(indexed=False, default=1)
	geo = ndb.GeoPtProperty(indexed=False, required=True)
	geohash = ndb.StringProperty(indexed=True, required=True)

	def update_geohash(self):
		"""
		Sets the geohash to correspond to the coordinates stored in self.geo.
		"""
		self.geohash = Geohash.encode(self.geo.lat, self.geo.lon, precision=20)

	def validate(self):
		"""Vaidates this model."""
		validate_parent(self, User)

		if self.category is None or len(self.category) == 0:
			raise BadValueError

		self.update_geohash()

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