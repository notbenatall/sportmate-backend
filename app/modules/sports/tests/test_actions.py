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
from testtools import DatastoreTest, HRDatastoreTest

import users.models as usermodels
import sports.models as models
import sports.actions as actions
import sports.messages as messages

def test_nothing():
    assert True == True

class TestGetAllSports(DatastoreTest):
    def test(self):

        cat1 = models.SportCategory(name='Ball')
        cat1.put()

        cat2 = models.SportCategory(name='Archery')
        cat2.put()

        cat3 = models.SportCategory(name='Football')
        cat3.add_parent(cat1)
        cat3.put()

        everything = actions.get_all_categories()

        assert type(everything) == messages.AllCategories
        assert len(everything.categories) == 3

        assert everything.categories[0].name == 'Archery'
        assert everything.categories[2].name == 'Football'
        assert len(everything.categories[2].parent_ids) == 1
        assert everything.categories[2].parent_ids[0] == cat1.key.id()
 

