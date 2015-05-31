"""
Sportmate API

Module: sports

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

from protorpc import messages
from protorpc import message_types


class Location(messages.Message):
	venue = messages.StringField(1, required=True)
	subvenue = messages.StringField(2)
	lat = messages.FloatField(3, required=True)
	lon = messages.FloatField(4, required=True)


class LocationCollection(messages.Message):
	locations = messages.MessageField(Location, 1, repeated=True)