"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds all the models.
"""

from google.appengine.ext import ndb
import geo.geomodel
from google.appengine.ext.db import BadValueError
from Crypto.Hash import SHA
import string
import random
import logging
from misc import validate_parent
from users.models import User
import Geohash


class SportCategory(ndb.Model):

    name = ndb.StringProperty(indexed=False, required=True)

    def __init__(self, **kwargs):

        if 'key' in kwargs:
            raise BadValueError

        super(SportCategory, self).__init__(**kwargs)

        if 'name' in kwargs:
            key = ndb.Key(SportCategory, self.name.lower())
            self.key = key

    def put(self):
        super(SportCategory, self).put()

    @staticmethod
    def get_by_name(name):
        key = ndb.Key(SportCategory, name.lower())
        cat = key.get()
        return cat

    @staticmethod
    def get_all():
        query = SportCategory.query()
        categories = query.fetch()
        return categories


class Sport(ndb.Model):
    """
    Parent: SportCategory
    """

    name = ndb.StringProperty(indexed=False, required=True)

    def __init__(self, **kwargs):

        if 'key' in kwargs:
            raise BadValueError

        super(Sport, self).__init__(**kwargs)

        if 'name' in kwargs:
            pairs = list(kwargs['parent'].pairs())
            pairs.append((Sport, self.name.lower()))
            key = ndb.Key(pairs=pairs)
            self.key = key

    def validate(self):
        """Validates this model."""
        validate_parent(self, SportCategory)

    def put(self):
        self.validate()
        super(Sport, self).put()

    @staticmethod
    def get_by_category_and_name(category, name):
        key = ndb.Key(SportCategory, category.lower(), Sport, name)
        sport = key.get()
        return sport

    @staticmethod
    def get_all():
        query = Sport.query()
        sports = query.fetch()
        return sports


class Game(ndb.Model):
    """
    Parent: User
    """

    sport = ndb.KeyProperty(kind=Sport, indexed=True, required=True)  
    players_full = ndb.BooleanProperty(indexed=True, default=False) 
    level = ndb.IntegerProperty(indexed=True, default=0)
    time = ndb.DateTimeProperty(indexed=True, required=True)
    name = ndb.StringProperty(indexed=False, required=True)
    players_needed = ndb.IntegerProperty(indexed=False, required=True)
    players_joined = ndb.IntegerProperty(indexed=False, default=1)
    geo = ndb.GeoPtProperty(indexed=False, required=True)
    geohash = ndb.StringProperty(indexed=True,required=True)

    def update_geohash(self):
        self.geohash = Geohash.encode(self.geo.lat, self.geo.lon, precision=20)

    def put(self):
        validate_parent(self, User)
        self.update_geohash()
        super(Game, self).put()


class SportProfile(ndb.Model):
    """
    Holds a users's information concerning a particular sport.

    Parent: User
    """

    sport = ndb.KeyProperty(kind=Sport, indexed=True, required=True)  
    level = ndb.IntegerProperty(indexed=True, default=0)

