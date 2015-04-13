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
from protorpc import messages
from protorpc import message_types


import facebook.models as models
import facebook.actions as actions
import users.models
import facebook.messages as fbmsgs

def test_nothing():
    assert True == True

