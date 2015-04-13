"""
Sportmate API

Module: sports

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

from protorpc import messages
from protorpc import message_types


class AllSports(messages.Message):
    categories = messages.MessageField(SportCategory, 1, repeated=True)

class SportCategory(messages.Message):
    name = messages.StringField(1)
    sports = messages.MessageField(Sport, 2, repeated=True)

class Sport(messages.Message):
    name = messages.StringField(1)
