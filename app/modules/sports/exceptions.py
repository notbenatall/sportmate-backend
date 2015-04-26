"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Defines custom exceptions for the sport module.
"""

class GameIsFullException(Exception):
	"""Thrown when adding a player to a game that is already full."""
	def __init__(self, message=""):
		super(GameIsFullException, self).__init__(message)