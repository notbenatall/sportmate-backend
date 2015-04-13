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

import facebook.models as models
import users.models as usermodels

def test_nothing():
    assert True == True

class BasicModelTest(object):
    def setup(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
 
    def teardown(self):
        self.testbed.deactivate()

class TestFacebookAccountModel(BasicModelTest):

    def setup(self):
        super(TestFacebookAccountModel, self).setup()

        # Create a default user to use for these tests
        self.user = usermodels.User(full_name = 'Silly Person')
        self.user.put()

    @raises(BadValueError)
    def testValidateModelFailure(self):
        account = models.FacebookAccount()
        account.validate()

    @raises(BadValueError)
    def testInsertWithoutValues(self):
        account = models.FacebookAccount()
        account.put()

    def testGetByFacebookId(self):
        account = models.FacebookAccount(parent = self.user.key)
        account.access_token = 'a token'
        account.facebook_id = 464193
        account.put()

        retreived_account = models.FacebookAccount.get_by_facebook_id(464193)

        assert_equals(retreived_account.facebook_id, 464193)

    def testGetByFacebookIdEmpty(self):
        retreived_account = models.FacebookAccount.get_by_facebook_id(987532576)
        assert retreived_account is None

    def testAssignUserAsParent(self):
        account = models.FacebookAccount(
            access_token = 'a token', 
            facebook_id = 1234675,
            parent = self.user.key)
        account.put()

        retreived_account = models.FacebookAccount.get_by_facebook_id(1234675)

        retrieved_parent = retreived_account.key.parent().get()

        assert retrieved_parent == self.user
        assert retrieved_parent.full_name == 'Silly Person'