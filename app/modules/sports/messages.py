"""
Sportmate API

Module: sports

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable=invalid-name,too-few-public-methods

from protorpc import messages


class SportCategory(messages.Message):
	"""Message containing a sports category."""
	name = messages.StringField(1)
	id = messages.StringField(2)
	parent_ids = messages.StringField(3, repeated=True)


class CategoryList(messages.Message):
	"""Message containing a list of categories."""
	categories = messages.MessageField(SportCategory, 1, repeated=True)
