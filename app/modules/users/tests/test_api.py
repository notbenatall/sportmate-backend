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

import users.models as models
import users.actions as actions
import users.messages as messages
import users.api

class TestAPI(HRDatastoreTest):
	def setup(self):

		super(TestAPI, self).setup()

		# Expose the api
		self.api = users.api.Users()

		# Put two users in the database and make
		# sure they are definitely accessable
		self.me = models.User(full_name = "Dicky Johnson")
		self.me.initialise_new_token()
		self.me.put()
		u = None
		while u is None:
			u = models.User.get_from_dumb_token(self.me.dumb_token)

		self.other_user = models.User(full_name = "Buck Billy")
		self.other_user.initialise_new_token()
		self.other_user.put()
		u = None
		while u is None:
			u = models.User.get_from_dumb_token(self.other_user.dumb_token)


class TestUserNotAuthenticating(TestAPI):

	@raises(UnauthorizedException)
	def test_friend_request(self):
		send = messages.UserId()
		relation = self.api.friend_request(send)


class TestFriendRequestNormal(TestAPI):
	def test_friend_request(self):

		send = messages.UserId(token=self.me.dumb_token, user= self.other_user.key.id())
		relation = self.api.friend_request(send)

		assert type(relation) is messages.Relationship
		assert self.me.key.id() in relation.users
		assert self.other_user.key.id() in relation.users
		assert relation.friend_request_sender_id == self.me.key.id()
		assert relation.is_friends == False
		assert relation.friend_request_sent
		

class TestFriendRequestDouble(TestAPI):
	def test_double_friend_request(self):

		send = messages.UserId(token=self.me.dumb_token, user= self.other_user.key.id())
		relation1 = self.api.friend_request(send)

		send = messages.UserId(token=self.other_user.dumb_token, user= self.me.key.id())
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

		send = messages.UserId(token=self.me.dumb_token, user= self.other_user.key.id())

		friends_list = self.api.get_friends_list(send)

		assert type(friends_list) is messages.FriendList
		assert len(friends_list.friends) == 1
		assert friends_list.friends[0] == self.me.key.id()


class TestUnFriend(TestAPI):

	def test_unfriend(self):

		send = messages.UserId(token=self.me.dumb_token, user= self.other_user.key.id())
		self.api.friend_request(send)

		send = messages.UserId(token=self.other_user.dumb_token, user= self.me.key.id())
		self.api.friend_request(send)

		relation = self.api.unfriend(messages.UserId(
						token=self.me.dumb_token,
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
			token=self.me.dumb_token, 
			user= self.other_user.key.id()))

		self.api.friend_request(messages.UserId(
			token=self.other_user.dumb_token, 
			user= self.me.key.id()))

		relation = self.api.get_relationship(messages.TwoUserIds(
			token = self.other_user.dumb_token, 
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
			token=self.me.dumb_token, 
			user= self.other_user.key.id()))

		relation = self.api.respond_to_friend_request(messages.FriendRequestResponse(
			token = self.other_user.dumb_token, 
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
			token=self.me.dumb_token, 
			user= self.other_user.key.id()))

		relation = self.api.respond_to_friend_request(messages.FriendRequestResponse(
			token = self.other_user.dumb_token, 
			user = self.me.key.id(),
			accept = False))

		assert type(relation) is messages.Relationship
		assert self.me.key.id() in relation.users
		assert self.other_user.key.id() in relation.users
		assert relation.friend_request_sender_id == self.me.key.id()
		assert relation.is_friends == False
		assert relation.friend_request_sent
		assert relation.friend_request_rejected
