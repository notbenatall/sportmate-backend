import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime
import endpoints
from google.appengine.ext.db import BadValueError
from endpoints import UnauthorizedException, NotFoundException
from testtools import DatastoreTest, HRDatastoreTest

import modules.users.models as models
import modules.users.actions as actions
import modules.users.messages as messages
import users.api

class TestAPI(HRDatastoreTest):
	def setup(self):

		super(TestAPI, self).setup()

		# Expose the api
		self.api = users.api.Users()

		# Put two users in the database and make
		# sure they are definitely accessable
		self.me = models.User(full_name = "Dicky Johnson", first_name="Dicky", facebook_id=1234)
		self.me.initialise_new_token()
		self.me.put()
		u = None
		while u is None:
			u = models.User.get_from_token(self.me.get_token())

		self.other_user = models.User(full_name = "Buck Billy", first_name="Buck")
		self.other_user.initialise_new_token()
		self.other_user.put()
		u = None
		while u is None:
			u = models.User.get_from_token(self.other_user.get_token())


class TestUserNotAuthenticating(TestAPI):

	@raises(UnauthorizedException)
	def test_friend_request(self):
		send = messages.UserId()
		relation = self.api.friend_request(send)


class TestFriendRequestNormal(TestAPI):
	def test_friend_request(self):

		send = messages.UserId(token=self.me.get_token(), user= self.other_user.key.id())
		relation = self.api.friend_request(send)

		assert type(relation) is messages.Relationship
		assert self.me.key.id() in relation.users
		assert self.other_user.key.id() in relation.users
		assert relation.friend_request_sender_id == self.me.key.id()
		assert relation.is_friends == False
		assert relation.friend_request_sent
		

class TestFriendRequestDouble(TestAPI):
	def test_double_friend_request(self):

		send = messages.UserId(token=self.me.get_token(), user= self.other_user.key.id())
		relation1 = self.api.friend_request(send)

		send = messages.UserId(token=self.other_user.get_token(), user= self.me.key.id())
		relation2 = self.api.friend_request(send)

		assert type(relation1) is messages.Relationship
		assert self.me.key.id() in relation1.users
		assert self.other_user.key.id() in relation1.users
		assert relation1.friend_request_sender_id == self.me.key.id()
		assert relation1.is_friends == False
		assert relation1.friend_request_sent

		assert type(relation2) is messages.Relationship
		assert self.me.key.id() in relation2.users
		assert self.other_user.key.id() in relation2.users
		assert relation2.friend_request_sender_id == self.me.key.id()
		assert relation2.is_friends == True
		assert relation2.friend_request_sent


class TestGetFriendList(TestAPI):

	def test_get_friend_list(self):

		actions._add_to_friends_list(self.me, self.other_user)

		send = messages.UserId(token=self.me.get_token(), user= self.other_user.key.id())

		friends_list = self.api.get_friends_list(send)

		assert type(friends_list) is messages.FriendList
		assert len(friends_list.friends) == 1
		assert friends_list.friends[0] == self.me.key.id()


class TestUnFriend(TestAPI):

	def test_unfriend(self):

		send = messages.UserId(token=self.me.get_token(), user= self.other_user.key.id())
		self.api.friend_request(send)

		send = messages.UserId(token=self.other_user.get_token(), user= self.me.key.id())
		self.api.friend_request(send)

		relation = self.api.unfriend(messages.UserId(
						token=self.me.get_token(),
						user= self.other_user.key.id()))


		assert type(relation) is messages.Relationship
		assert self.me.key.id() in relation.users
		assert self.other_user.key.id() in relation.users
		assert relation.friend_request_sender_id == self.me.key.id()
		assert relation.is_friends == False
		assert relation.friend_request_sent
		assert relation.friend_unfriender_id == self.me.key.id()


class TestGetRelationship(TestAPI):

	def test_get_relationship(self):

		self.api.friend_request(messages.UserId(
			token=self.me.get_token(), 
			user= self.other_user.key.id()))

		self.api.friend_request(messages.UserId(
			token=self.other_user.get_token(), 
			user= self.me.key.id()))

		relation = self.api.get_relationship(messages.TwoUserIds(
			token = self.other_user.get_token(), 
			userA = self.me.key.id(),
			userB = self.other_user.key.id()))

		assert type(relation) is messages.Relationship
		assert self.me.key.id() in relation.users
		assert self.other_user.key.id() in relation.users
		assert relation.friend_request_sender_id == self.me.key.id()
		assert relation.is_friends == True
		assert relation.friend_request_sent


class TestRespondToFriendRequestAccept(TestAPI):
	def test(self):

		self.api.friend_request(messages.UserId(
			token=self.me.get_token(), 
			user= self.other_user.key.id()))

		relation = self.api.respond_to_friend_request(messages.FriendRequestResponse(
			token = self.other_user.get_token(), 
			user = self.me.key.id(),
			accept = True))

		assert type(relation) is messages.Relationship
		assert self.me.key.id() in relation.users
		assert self.other_user.key.id() in relation.users
		assert relation.friend_request_sender_id == self.me.key.id()
		assert relation.is_friends == True
		assert relation.friend_request_sent
		assert not relation.friend_request_rejected

class TestRespondToFriendRequestDecline(TestAPI):
	def test(self):

		self.api.friend_request(messages.UserId(
			token=self.me.get_token(), 
			user= self.other_user.key.id()))

		relation = self.api.respond_to_friend_request(messages.FriendRequestResponse(
			token = self.other_user.get_token(), 
			user = self.me.key.id(),
			accept = False))

		assert type(relation) is messages.Relationship
		assert self.me.key.id() in relation.users
		assert self.other_user.key.id() in relation.users
		assert relation.friend_request_sender_id == self.me.key.id()
		assert relation.is_friends == False
		assert relation.friend_request_sent
		assert relation.friend_request_rejected


class TestGetUser(TestAPI):
	def test_get_me(self):

		send = messages.UserId(token=self.me.get_token())
		myself = self.api.get_user(send)

		#assert myself.token == self.me.get_token()
		assert myself.facebook_id == 1234


class TestUserSearch(DatastoreTest):

    def setup(self):
        super(TestUserSearch, self).setup()

        # Expose the api
        self.api = users.api.Users()

        self.adrian = models.User(full_name='Adrian Letchford', first_name="Adrian")
        self.adrian.initialise_new_token()
        self.adrian.put()

        self.tom = models.User(full_name='Tom Haleminh', first_name="Tom")
        self.tom.put()


    def test_search_for_adrian(self):
        
        request = messages.UserSearch(token=self.adrian.get_token(), term="ad")

        result = self.api.user_search(request)
        users = result.users

        assert len(users) == 1
        assert users[0].full_name == "Adrian Letchford"

class TestGetNearbyUsers(DatastoreTest):

    def setup(self):
        super(TestGetNearbyUsers, self).setup()

        # Expose the api
        self.api = users.api.Users()

        self.adrian = models.User(full_name='Adrian Letchford', first_name="Adrian")
        self.adrian.initialise_new_token()
        self.adrian.put()

        self.tom = models.User(full_name='Tom Haleminh', first_name="Tom")
        self.tom.put()

        self.barney = models.User(full_name='Barney', first_name="Barney")
        self.barney.put()


    def test(self):

    	request = messages.UserSearch(token=self.adrian.get_token())

    	userList = self.api.get_nearby_users(request)

        assert userList.users[0].first_name == "Adrian"
        assert userList.users[1].first_name == "Tom"
