"""
Sportmate API v1

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds the models for users.
"""

from google.appengine.ext import ndb
import geo.geomodel
from google.appengine.ext.db import BadValueError
from Crypto.Hash import SHA
import string
import random
import logging
import misc # sportmate's misc module

class User(ndb.Model):

    dumb_token = ndb.StringProperty(indexed=True)
    searchable_name = ndb.StringProperty(indexed=True, required=True)
    
    full_name = ndb.StringProperty(indexed=False, required=True)
    email = ndb.StringProperty(indexed=False, required=False)

    @staticmethod
    def generate_token(salt):
        """Generates a random token."""
        sha = SHA.new()
        sha.update(salt)
        sha.update(misc.random_string()) 
        token = sha.hexdigest()
        return token

    def initialise_new_token(self):
        self.dumb_token = self.generate_token(str(self.key))
        return self.dumb_token

    @staticmethod
    def get_from_dumb_token(token):
        q = User.query(User.dumb_token == token)
        user = q.get()
        return user

    def put(self):
        """Overrides the default put() behaviour to setup automatic fields."""
        
        # Set the searchable name
        if self.full_name is None:
            raise BadValueError
        self.searchable_name = self.full_name.lower()

        super(User, self).put()


class Relationship(ndb.Model):
    """
    Models the relationship between two users.
    """
    
    users = ndb.KeyProperty(kind=User, indexed=True, repeated=True)
    is_friends = ndb.BooleanProperty(indexed=True, default=False)

    friend_request_sent = ndb.BooleanProperty(indexed=False, default=False)
    friend_request_sender = ndb.KeyProperty(kind=User, indexed=False)
    friend_request_rejected = ndb.BooleanProperty(indexed=False, default=False)
    friend_unfriender = ndb.KeyProperty(kind=User, indexed=False)

    created = ndb.DateTimeProperty(auto_now_add=True)

    def validate(self):
        """Validates this model."""

        # Make sure this relationship has exactly two users before writing to
        # the database.
        if len(self.users) != 2:
            raise BadValueError

    @staticmethod
    def _key_from_users(userA, userB):
        """
        Creates a Relationship key from two users. The key contains both users 
        as kinds. The users are sorted before creating the key such that create
        (A, B) == create(B, A). This means that the key technically does have 
        a parent, but the parent key does not correspond to any entities.
        """
        user_ids = [str(userA.key.id()), str(userB.key.id())]
        user_ids.sort()
        key = ndb.Key(User, user_ids[0], User, user_ids[1], 
            Relationship, ''.join(user_ids))
        return key

    @staticmethod
    def create(userA, userB):
        """
        Creates a new Relationship between two users. The relationship's key
        prevents the entity from having a parent. See _key_from_users().
        """
        relationship = Relationship(
            key=Relationship._key_from_users(userA, userB), 
            users=[userA.key, userB.key])
        return relationship

    def put(self):
        """Overrides the default put() behaviour."""
        self.validate()
        super(Relationship, self).put()

    @staticmethod
    def get_by_users(userA, userB):
        key = Relationship._key_from_users(userA, userB)
        relationship = key.get()
        return relationship
        # q = Relationship.query(ndb.AND(Relationship.users == userA.key, Relationship.users == userB.key))
        # users = q.get()
        # return users



class FriendList(ndb.Model):
    """
    Stores a list of some of a person's friends for faster and cheaper lookup.
    There is a limit of 5000 on the number of users that can be stored in each
    individual list model. Users with more than 5,000 friends will need to have
    multiple indexes. 

    Parent: User
    """

    friends = ndb.KeyProperty(kind=User, indexed=True, repeated=True)
    full = ndb.BooleanProperty(indexed=True, default=False) 

    def validate(self):
        """Validates this model."""

        misc.validate_parent(self, User)

        if len(self.friends) > 5000:
            raise BadValueError

    def put(self):
        self.validate()
        super(FriendList, self).put()

    def add_friend(self, user):

        if len(self.friends) >= 5000:
            raise Exception("Full.")

        self.friends.append(user)

        if len(self.friends) == 5000:
            self.full = True
        else:
            self.full = False

    @staticmethod
    def get_or_create_addable_friend_list(user):
        query = FriendList.query(ancestor=user.key)
        query.filter(FriendList.full == False)
        friend_list = query.get()

        if friend_list is None:
            friend_list = FriendList(parent=user.key)

        return friend_list
