"""
Sportmate API

Module: facebook

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable=too-few-public-methods

from protorpc import messages
from protorpc import message_types

import modules.users.messages


class Url(messages.Message):
	"""Message containing a URL."""
	url = messages.StringField(1)

class Code(messages.Message):
	"""Message containing Facebook's client authentication code."""
	code = messages.StringField(1)

class FacebookAccountWithUser(messages.Message):
	"""
	Message containing a Facebook account with the corresponding
	Sportmate user.
	"""
	facebook_id = messages.IntegerField(1)
	access_token = messages.StringField(2)
	expires = message_types.DateTimeField(3)
	user = messages.MessageField(modules.users.messages.UserMe, 4)