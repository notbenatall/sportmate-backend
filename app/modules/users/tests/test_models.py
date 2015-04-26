import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.ext.db import BadValueError
import testtools

import modules.users.models as models

def test_nothing():
	assert True == True

class TestUserModel(testtools.DatastoreTest):

	@raises(BadValueError)
	def testInsertUserWithoutName(self):
		models.User().put()

	def testSetName(self):
		user = models.User(full_name="John Clease", first_name="John")
		assert_equals('John Clease', user.full_name)

	def testSearchableNameUponUserInsert(self):
		user = models.User(full_name="Dicky Johnson", first_name="Dicky")
		user.put()
		assert_equals('dicky johnson', user.searchable_name)

	def testInsertUser(self):
		user = models.User(full_name="John Clease", first_name="John")
		user.put()
		result = models.User.query().fetch(2)   
		assert_equals(1, len(result))
		assert_equals('John Clease', result[0].full_name)

	def testGenerateNewToken(self):
		token = models.User.generate_token('someinterestingsalt')
		assert type(token) is str
		assert len(token) == 40

	def testInitialiseNewToken(self):
		user = models.User()
		user.initialise_new_token()
		assert type(user.dumb_token) is str
		assert len(user.dumb_token) == 40

	def testUserType(self):
		user = models.User()
		assert type(user) is models.User

	def test_no_token(self):
		user = models.User(full_name = 'a name', first_name="a")
		user.put()

		token = user.get_token()

		assert token is None

	def test_get_from_token(self):
		user = models.User(full_name = 'a name', first_name="a")
		user.initialise_new_token()
		user.put()
		token = user.get_token()

		ruser = models.User.get_from_token(token)

		assert ruser == user



class TestRelationshipModel(testtools.DatastoreTest):

	def setup(self):
		super(TestRelationshipModel, self).setup()

		# Create default users to use for these tests
		self.usera = models.User(full_name = 'Rowan Atkinson', first_name="Rowan")
		self.usera.put()

		self.userb = models.User(full_name = 'Stephen Fry', first_name="Stephan")
		self.userb.put()

	@raises(BadValueError)
	def testValidateModelFailure(self):
		relation = models.Relationship()
		relation.validate()

	@raises(BadValueError)
	def testPutEmptyModel(self):
		relation = models.Relationship()
		relation.put()

	def test_create_associative_key(self):
		key1 = models.Relationship._key_from_users(self.usera, self.userb)
		key2 = models.Relationship._key_from_users(self.userb, self.usera)
		assert key1 == key2

	def test_create(self):
		relationship = models.Relationship.create(self.usera, self.userb)
		assert type(relationship) is models.Relationship
		assert self.usera.key in relationship.users
		assert self.userb.key in relationship.users

	def testDefaultValues(self):
		relation = models.Relationship()
		assert relation.is_friends == False

	def testCreatedField(self):
		relation = models.Relationship.create(self.usera, self.userb)
		relation.put()

		assert type(relation.created) is datetime

	@raises(BadValueError)
	def testPutFullModel(self):
		relation = models.Relationship()
		relation.users.append(self.usera)
		relation.users.append(self.userb)
		relation_key = relation.put() 

	def testGetByUsers(self):
		relation = models.Relationship.create(self.usera, self.userb)
		relation_key = relation.put()
		retrieved_relation = models.Relationship.get_by_users(self.usera, self.userb)

		assert type(retrieved_relation.users) is list
		assert retrieved_relation.users[0] == self.usera.key
		assert retrieved_relation.users[1] == self.userb.key


	def testGetByUsersEmpty(self):
		usera = models.User(full_name = 'Rowan Atkinson', first_name="Rowan")
		usera.put()
		userb = models.User(full_name = 'Stephen Fry', first_name="Stephen")
		userb.put()
		relationship = models.Relationship.get_by_users(self.usera, self.userb)

		assert relationship is None


class TestFriendListModel(testtools.DatastoreTest):

	@raises(BadValueError)
	def testValidateModelFailure(self):
		flist = models.FriendList()
		flist.validate()

	@attr(slow=True)
	@raises(BadValueError)
	def test_put_overfull_model(self):
		flist = models.FriendList()
		for i in range(5001):
			flist.friends.append(models.User())
		flist.put()

	@attr(slow=True)
	@raises(BadValueError)
	def testValidateFailOnMoreThan5000Users(self):
		flist = models.FriendList()
		for i in range(5001):
			flist.friends.append(models.User())
		flist.validate()

	def test_get_or_create_first_time(self):
		user = models.User(full_name = 'Rowan Atkinson', first_name="Rowan")
		user.put()

		friend_list = models.FriendList.get_or_create_addable_friend_list(user)

		assert type(friend_list) is models.FriendList
		assert len(friend_list.friends) < 5000