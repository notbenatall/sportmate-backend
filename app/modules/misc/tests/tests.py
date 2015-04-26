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

import misc

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


class testGeneral(DatastoreTest):

    def testValidateParentIsUser(self):
        p = BlankParentModel()
        p.put()
        m = BlankModel(parent=p.key)
        misc.validate_parent(m, BlankParentModel)