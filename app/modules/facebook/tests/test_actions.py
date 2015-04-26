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
from testtools import DatastoreTest

import modules.facebook.models as models
import modules.facebook.actions as actions
import modules.users.models as usermodels

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
		assert type(account_parent) is usermodels.User
		assert account_parent.facebook_id == 572659283
		assert_equals(account_parent.full_name, 'John Clease')