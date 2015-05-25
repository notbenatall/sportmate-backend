"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds various helpful codesnippets
"""

import os
from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from google.appengine.api.app_identity import get_application_id
import string
import random
from socket import socket, SOCK_DGRAM, AF_INET 

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
	"""Generates a random string of characters."""
	return ''.join(random.choice(chars) for _ in range(size))

def validate_parent(instance, parent_type):
	"""Throws a BadValueError if the instance's parent is not a parent_type."""

	if not issubclass(type(instance), ndb.Model):
		raise Exception("This is not a model.")

	if not hasattr(instance.key, 'parent') or \
		instance.key.parent().kind() != parent_type.__name__:
		raise BadValueError



def is_development():
	"""Checks to see if this is the development sever."""

	if 'SERVER_SOFTWARE' in os.environ and \
		os.environ['SERVER_SOFTWARE'].startswith('Development'):
		return True

	return False

def is_development_testing():
	"""Checks to see if this is a testing environment."""

	if 'SERVER_SOFTWARE' in os.environ and \
		os.environ['SERVER_SOFTWARE'].startswith('Dev test'):
		return True

	return False

def is_test():
	"""Checks to see if this is a test sever."""
	appname = get_application_id()

	if "test" in appname:
		return True

	return False



def get_ip():
	"""Return the ip of the running computer."""
	s = socket(AF_INET, SOCK_DGRAM) 
	s.connect(('google.com', 0)) 

	IP = s.getsockname()[0]
	return IP