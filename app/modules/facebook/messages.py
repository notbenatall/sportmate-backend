"""
Sportmate API

Module: facebook

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

from protorpc import messages
from protorpc import message_types

import users.messages


class UrlMessage(messages.Message):
    url = messages.StringField(1)

class CodeMessage(messages.Message):
    code = messages.StringField(1)

class FacebookAccountWithUser(messages.Message):
	facebook_id = messages.IntegerField(1)
	access_token = messages.StringField(2)
	expires = message_types.DateTimeField(3)
	user = messages.MessageField(users.messages.UserMe, 4)