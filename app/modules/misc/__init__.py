"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds various helpful codesnippets
"""

from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
import string
import random

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