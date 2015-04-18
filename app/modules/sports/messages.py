"""
Sportmate API

Module: sports

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

from protorpc import messages
from protorpc import message_types


class SportCategory(messages.Message):
    name = messages.StringField(1)
    id = messages.StringField(2)
    parent_ids = messages.StringField(3, repeated=True)


class AllCategories(messages.Message):
    categories = messages.MessageField(SportCategory, 1, repeated=True)
