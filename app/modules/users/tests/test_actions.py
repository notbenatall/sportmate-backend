import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util
import testtools
from google.appengine.ext.db import BadValueError
from endpoints import UnauthorizedException, NotFoundException

import modules.users.models as models
import modules.users.actions as actions

def test_nothing():
    assert True == True

class TestSimpleStuff(testtools.DatastoreTest):

    @raises(UnauthorizedException)
    def testVerifyAndGetUserFail(self):
        actions.verify_and_get_user(token='nothing')

    def test_verify_and_get_user(self):
        user = models.User(full_name='hello', first_name="hello")
        user.initialise_new_token()
        user.put()

        result = actions.verify_and_get_user(token=user.get_token())

        assert user == result

class TestFriendships(testtools.HRDatastoreTest):

    def setup(self):
        super(TestFriendships, self).setup()

        self.sender = models.User(full_name='hello', first_name="hello")
        self.sender.put()

        self.reciever = models.User(full_name='hello2', first_name="hello2")
        self.reciever.put()

    def assert_in_friends_list(self):
        friend_list_sender = models.FriendList.get_or_create_addable_friend_list(self.sender)
        friend_list_reciever = models.FriendList.get_or_create_addable_friend_list(self.reciever)

        assert self.reciever.key in friend_list_sender.friends
        assert self.sender.key in friend_list_reciever.friends

    def assert_not_in_friends_list(self):
        friend_list_sender = models.FriendList.get_or_create_addable_friend_list(self.sender)
        friend_list_reciever = models.FriendList.get_or_create_addable_friend_list(self.reciever)

        assert self.reciever.key not in friend_list_sender.friends
        assert self.sender.key not in friend_list_reciever.friends


class TestFriendRequest(TestFriendships):

    @raises(NotFoundException)
    def test_fail_on_unknown_users(self):
        actions.friend_request(76576533, 8768665)

    def test_created_friend_request(self):

        actions.friend_request(self.sender.key.id(), self.reciever.key.id())

        relation = models.Relationship.get_by_users(self.sender, self.reciever)

        assert relation is not None
        assert relation.friend_request_sent == True

    def test_send_friend_request_after_already_recieved(self):
        actions.friend_request(self.reciever.key.id(), self.sender.key.id())
        actions.friend_request(self.sender.key.id(), self.reciever.key.id())

        relation = models.Relationship.get_by_users(self.sender, self.reciever)

        assert relation is not None
        assert relation.is_friends == True


class TestRespondToFriendRequest(TestFriendships):

    @raises(NotFoundException)
    def respond_to_friend_request(self):
        actions.friend_request(76576533, 8768665, False)

    def test_accept_friend_request(self):
        actions.friend_request(self.sender.key.id(), self.reciever.key.id())
        actions.respond_to_friend_request(self.reciever.key.id(), self.sender.key.id(), True)
        relation = models.Relationship.get_by_users(self.sender, self.reciever)

        assert relation.is_friends == True 
        assert not relation.friend_request_rejected

        self.assert_in_friends_list()

    def test_reject_friend_request(self):
        actions.friend_request(self.sender.key.id(), self.reciever.key.id())
        actions.respond_to_friend_request(self.reciever.key.id(), self.sender.key.id(), False)
        relation = models.Relationship.get_by_users(self.sender, self.reciever)

        assert not relation.is_friends
        assert relation.friend_request_rejected

class TestAddToFriendList(TestFriendships):

    def test_add_to_friend_list(self):
        actions._add_to_friends_list(self.sender, self.reciever)

        self.assert_in_friends_list()

class TestRemoveFromFriendList(TestFriendships):

    def test_remove_from_friend_list(self):
        actions._add_to_friends_list(self.sender, self.reciever)
        actions._remove_from_friends_list(self.sender, self.reciever)

        self.assert_not_in_friends_list()

class TestUnfriend(TestFriendships):

    def test_non_friends(self):
        relationship = actions.unfriend(self.sender.key.id(), self.reciever.key.id())

        assert type(relationship) is models.Relationship
        self.assert_not_in_friends_list()
        assert relationship.is_friends == False


class TestUnfriend2(TestFriendships):

    def test_friends(self):
        actions.friend_request(self.sender.key.id(), self.reciever.key.id())
        actions.respond_to_friend_request(self.reciever.key.id(), self.sender.key.id(), True)
        self.assert_in_friends_list()

        relationship = actions.unfriend(self.sender.key.id(), self.reciever.key.id())
        
        assert relationship.key.kind() == "Relationship"
        self.assert_not_in_friends_list()
        assert relationship.is_friends == False
        assert relationship.friend_unfriender == self.sender.key

class TestUserKeyIdToUser(testtools.DatastoreTest):

    def setup(self):
        super(TestUserKeyIdToUser, self).setup()

        self.user = models.User(full_name='Stephen Fry', first_name="Stephen")
        self.user.put()

    @raises(TypeError)
    def test_user_key_id_to_user_on_bool(self):
        user = actions.user_key_id_to_user(True)

    def test_user_key_id_to_user_on_User(self):
        retrieved_user = actions.user_key_id_to_user(self.user)
        assert retrieved_user == self.user

    def test_user_key_id_to_user_on_Key(self):
        retrieved_user = actions.user_key_id_to_user(self.user.key)
        assert retrieved_user == self.user

    def test_user_key_id_to_user_on_Id(self):
        retrieved_user = actions.user_key_id_to_user(self.user.key.id())
        assert retrieved_user == self.user

    @raises(NotFoundException)
    def test_user_key_id_to_user_on_Id_not_found(self):
        retrieved_user = actions.user_key_id_to_user('flubadabadub')



class TestGetRelationship(TestFriendships):

    def test_get_not_friends(self):
        relation = actions.get_relationship(self.sender, self.reciever)
        assert relation.is_friends == False

    def test_get_friends(self):
        actions.friend_request(self.sender.key.id(), self.reciever.key.id())
        actions.respond_to_friend_request(self.reciever.key.id(), self.sender.key.id(), True)

        relation = actions.get_relationship(self.sender, self.reciever)
        assert relation.is_friends == True

    
class TestGetFriendList(TestFriendships):

    def test_get_empty_friends_list(self):
        flist = actions.get_friends_list(self.sender)
        assert len(flist.friends) == 0

    def test_get_friends_list(self):

        actions._add_to_friends_list(self.sender, self.reciever)

        flist = actions.get_friends_list(self.sender)
        assert len(flist.friends) == 1