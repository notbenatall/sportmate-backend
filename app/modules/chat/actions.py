"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds all the actions for the chat module.
"""

from google.appengine.ext import ndb
import modules.chat.models as models
import modules.chat.messages as messages
from modules.users.actions import user_key_id_to_user, user_to_message



def auth_chat_message_to_model(message, auth_user):
	"""
	Converts a messages.AuthChatMessage to a models.ChatMessage.
	"""
	model = models.ChatMessage()
	model.message_id = message.message_id
	model.body = message.body

	model.sender_id = auth_user.key.id()
	model.sender_first_name = auth_user.first_name
	model.sender_full_name = auth_user.full_name

	purl = "https://graph.facebook.com/%d/picture?type=large"
	model.sender_profile_image = purl % auth_user.facebook_id

	for r_id in message.recipients:
		model.add_recipient(r_id)

	return model

def auth_chat_message_to_chat_message(auth_msg, auth_user): # pylint: disable=invalid-name
	"""
	Converts a AuthChatMessage to a ChatMessage
	"""
	msg = messages.ChatMessage()
	msg.message_id = auth_msg.message_id
	msg.body = auth_msg.body
	msg.recipients = auth_msg.recipients
	msg.parent_key = auth_msg.parent_key

	msg.sender_id = auth_user.key.id()
	msg.sender_first_name = auth_user.first_name
	msg.sender_full_name = auth_user.full_name

	purl = "https://graph.facebook.com/%d/picture?type=large"
	msg.sender_profile_image = purl % auth_user.facebook_id

	return msg

def model_to_chat_message(model):
	"""
	Converts a models.ChatMessage to a messages.ChatMessage.
	"""
	msg = messages.ChatMessage()
	msg.message_id = model.message_id
	msg.body = model.body
	msg.recipients = [long(ID) for ID in model.recipients.split(",")]

	msg.sender_id = model.sender_id
	msg.sender_first_name = model.sender_first_name
	msg.sender_full_name = model.sender_full_name
	msg.sender_profile_image = model.sender_profile_image

	return msg


@ndb.transactional(xg=True)
def add_message(msg, auth_user):
	"""Adds a message to the system."""
	model = auth_chat_message_to_model(msg, auth_user)
	parent_key = ndb.Key(urlsafe=msg.parent_key)
	models.Thread.add_message(parent_key, model)

	return msg

@ndb.transactional(xg=True)
def get_messages(parent_key):
	"""Returns a list of the latest messages in a thread."""
	number = models.Thread.get_current_thread_number(parent_key)

	msg = messages.ChatMessageList()

	if number is None:
		msg.messages = []
	else:
		thread = models.Thread.get_by_key(parent_key, number)
		msg.messages = [model_to_chat_message(m) for m in thread.messages]

	return msg


def get_two_user_thread(auth_user, other_user):
	"""
	Returns the thread key for the authenticating user and another user.
	"""

	other_user = user_key_id_to_user(other_user)

	user_keys = [auth_user.key, other_user.key]
	thread_key = models.Thread.make_private_group_parent(user_keys)

	msg = messages.Thread()
	msg.key = thread_key.urlsafe()
	msg.participants = [user_to_message(u) for u in [auth_user, other_user]]

	return msg