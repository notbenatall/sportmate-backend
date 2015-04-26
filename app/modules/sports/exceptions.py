"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Defines custom exceptions for the sport module.
"""

from endpoints import NotFoundException
from google.appengine.ext.db import BadValueError


class GameIsFullException(BadValueError):
	def __init__(self, message=""):
		super(GameIsFullException, self).__init__(message)