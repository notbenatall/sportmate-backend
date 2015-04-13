import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime

# Allow access to the GAE modules
sys.path.append('/home/adrian/Development/google_appengine')

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.ext.db import BadValueError

# Allow access to the modules made available to this app
sys.path.append('../../../lib')
sys.path.append('../../../modules')

import misc

# Turn off logging. Google App Engine spits out all kinds of junk which we
# don't need.
logger = logging.getLogger()
logger.disabled = True

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

class BlankParentModel(ndb.Model):
	pass

class BlankModel(ndb.Model):
	pass

@raises(BadValueError)
def testValidateParentFailure():

    m = BlankModel()
    misc.validate_parent(m, BlankParentModel)

def testRandomString():
    s = misc.random_string(10)
    assert type(s) is str 
    assert_equals(len(s), 10)


class testGeneral(BasicModelTest):

    def testValidateParentIsUser(self):
        p = BlankParentModel()
        p.put()
        m = BlankModel(parent=p.key)
        misc.validate_parent(m, BlankParentModel)

if __name__ == '__main__':
    # Run all the tests in this file
    module_name = sys.modules[__name__].__file__
    result = nose.run(argv=[sys.argv[0], module_name, '-v'])