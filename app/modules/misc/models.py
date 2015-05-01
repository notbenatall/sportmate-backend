"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from endpoints import NotFoundException


def get_model(obj, model_type):
	"""
	Takes either a model, key or id and returns the corresponding model.
	"""

	if type(obj) is model_type:
		value = obj
	elif type(obj) is ndb.Key:
		value = obj.get()
	elif type(obj) is long or type(obj) is int or type(obj) is str:
		value = model_type.get_by_id(obj)
	else:
		raise TypeError("Unknown type.")
	if value is None:
		raise NotFoundException()
	if type(value) is not model_type:
		raise BadValueError()

	return value