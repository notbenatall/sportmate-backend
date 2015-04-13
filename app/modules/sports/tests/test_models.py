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

class TestSportModel(BasicModelTest):

    @raises(BadValueError)
    def testValidateModelFailure(self):
        sport = models.Sport()
        sport.validate()

    @raises(BadValueError)
    def testEmptyPut(self):
        sport = models.Sport()
        sport.put()

    def testBasicPut(self):
        cat = models.SportCategory(name='Basket Ball')
        cat.put()

        sport = models.Sport(name='Basket Ball', parent = cat.key)
        sport.put()

    def test_get_by_category_and_name(self):

        cat = models.SportCategory(name='Cycling')
        cat.put()

        sport = models.Sport(name='Unicyling', parent = cat.key)
        sport.put()

        retrieved_sport = models.Sport.get_by_category_and_name('cycling', 'unicyling')

        assert retrieved_sport == sport

class TestSportCategoryModelGetAll(BasicModelTest):
    def test(self):

        cat = models.SportCategory(name='Cycling')
        cat.put()

        categories = models.SportCategory.get_all()

        assert len(categories) == 1
        assert categories[0].name == 'Cycling'

class TestSportModelGetAll(BasicModelTest):
    def test(self):

        cat = models.SportCategory(name='Cycling')
        cat.put()

        sport = models.Sport(name='Unicyling', parent = cat.key)
        sport.put()

        sports = models.Sport.get_all()

        assert len(sports) == 1
        assert sports[0].name == 'Unicyling'



class TestGameModel(BasicModelTest):

    def testBasicPut(self):
        user = usermodels.User(full_name = 'Rowan Atkinson')
        user.put()

        cat = models.SportCategory(name='category')
        cat.put()

        sport = models.Sport(name='a sport', parent = cat.key)
        sport.put()

        game = models.Game(
            name='Basket Ball',
            sport = sport.key,
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