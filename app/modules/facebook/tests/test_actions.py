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
import facebook.actions as actions
import users.models

def test_nothing():
    assert True == True

class DatastoreTest(object):
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


def testGetLoginUrl():
	url = actions.get_login_url('some_redirect')
	assert type(url) is str
	assert url.startswith('https://')

class testWithDatastore(DatastoreTest):

	def testCreateNewUser(self):

		profile = {
			'name': 'John Clease',
			'email': 'john@python.com',
			'expires': datetime.now(),
			'id': '572659283'
		}
		access_token = 'sometoken'

		account = actions._create_new_user(profile, access_token)
		account_parent = account.key.parent().get()

		assert type(account) is models.FacebookAccount
		assert type(account_parent) is users.models.User
		assert_equals(account_parent.full_name, 'John Clease')