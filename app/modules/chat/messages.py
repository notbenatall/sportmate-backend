"""
Sportmate API

Module: chat

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable=invalid-name,too-few-public-methods,too-many-instance-attributes

from protorpc import messages
from protorpc import message_types
from modules.users.messages import User

class ChatMessage(messages.Message):
	"""A IM chat message."""
	body = messages.StringField(1, required=True)
	recipients = messages.IntegerField(2, repeated=True)
	parent_key = messages.StringField(3, required=True)
	message_id = messages.StringField(4, required=True)
	sender_first_name = messages.StringField(5, required=True)
	sender_full_name = messages.StringField(6, required=True)
	sender_profile_image = messages.StringField(7, required=True)
	sender_id = messages.IntegerField(8, required=True)
	timestamp = message_types.DateTimeField(9, required=True)


class AuthChatMessage(messages.Message):
	"""A IM chat message."""
	body = messages.StringField(1, required=True)
	recipients = messages.IntegerField(2, repeated=True)

	parent_key = messages.StringField(4, required=True)

	token = messages.StringField(5, required=True)
	message_id = messages.StringField(6, required=True)


class ChatMessageList(messages.Message):
	"""A message containg a list of chat messages."""
	messages = messages.MessageField(ChatMessage, 1, repeated=True)


class ChatMessageRequest(messages.Message):
	"""A request for a list of chat messages."""
	token = messages.StringField(1, required=True)
	parent_key = messages.StringField(2, required=True)


class Thread(messages.Message):
	"""
	Contains the details for a chat thread.
	"""
	participants = messages.MessageField(User, 1, repeated=True)
	key = messages.StringField(2, required=True)