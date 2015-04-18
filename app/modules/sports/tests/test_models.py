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

import users.models as usermodels
import sports.models as models

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



class TestSportCategoryModel(BasicModelTest):

    @raises(BadValueError)
    def testEmptyPut(self):
        cat = models.SportCategory()
        cat.put()

    def testBasicPut(self):
        cat = models.SportCategory(name='Basket Ball')
        cat.put()

    def testRetrieveByFullName(self):
        cat = models.SportCategory(name='Basket Ball')
        cat.put()
        retrieved_cat = models.SportCategory.get_by_name('Basket Ball')
        assert retrieved_cat == cat

    def test_add_parent(self):
        cat1 = models.SportCategory(name='Ball')

        cat2 = models.SportCategory(name='Basket Ball')
        cat2.add_parent(cat1)

        cat3 = models.SportCategory(name='Extreme Basket Ball')
        cat3.add_parent(cat2)

        assert cat2.paths[0] == cat1.key
        assert cat1.key in cat2.parents
        assert cat3.paths[0] == ndb.Key(pairs=[cat1.key.pairs()[0], cat2.key.pairs()[0]])
        assert cat2.key in cat3.parents


class TestSportCategoryModelGetAll(BasicModelTest):
    def test(self):

        cat = models.SportCategory(name='Cycling')
        cat.put()

        categories = models.SportCategory.get_all()

        assert len(categories) == 1
        assert categories[0].name == 'Cycling'


class TestGameModel(BasicModelTest):

    def testBasicPut(self):
        user = usermodels.User(full_name = 'Rowan Atkinson')
        user.put()

        cat = models.SportCategory(name='category')
        cat.put()

        game = models.Game(
            name='Basket Ball',
            category = [cat.key],
            players_needed=5,
            geo=ndb.GeoPt(37, -122),
            time = datetime.now(),
            parent = user.key
            )
        game.put()

    @raises(BadValueError)
    def test_missing_category(self):
        user = usermodels.User(full_name = 'Rowan Atkinson')
        user.put()

        game = models.Game(
            name='Basket Ball',
            players_needed=5,
            geo=ndb.GeoPt(37, -122),
            time = datetime.now(),
            parent = user.key
            )
        game.put()


    def test_update_geohash(self):

        game = models.Game(
            geo=ndb.GeoPt(37, -122),
            )

        game.update_geohash()

        assert type(game.geohash) is str 
        assert len(game.geohash) == 20