"""
Sportmate API

Module: chat

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable=no-self-use, no-init

import endpoints
from protorpc import remote
from google.appengine.ext import ndb

from modules.users.actions import verify_and_get_user
import modules.chat.actions as actions
import modules.chat.messages as messages
from modules.users.messages import UserId
from modules.misc.messages import TextMessage

import modules.api

@modules.api.API.api_class(resource_name='chat')
class Chat(remote.Service):
	"""
	Access and modify IM chat.
	"""
	@endpoints.method(messages.AuthChatMessage, messages.ChatMessage,
		path='messages/add', http_method='POST', name='addmessage')
	def add_message(self, request):
		"""Send a friend request."""
		auth_user = verify_and_get_user(token=request.token)

		msg = actions.add_message(request, auth_user)

		return actions.auth_chat_message_to_chat_message(msg, auth_user)

	@endpoints.method(messages.ChatMessageRequest, messages.ChatMessageList,
		path='messages/get', http_method='POST', name='getmessages')
	def get_messages(self, request):
		"""Send a friend request."""
		verify_and_get_user(token=request.token)

		msg = actions.get_messages(ndb.Key(urlsafe=request.parent_key))

		return msg


	@endpoints.method(UserId, messages.Thread,
		path='thread/get_user_thread_id', http_method='POST', name='getuserthreadid')
	def get_user_thread_key(self, request):
		"""Returns the key to the thread between the authenticating user and another."""
		auth_user = verify_and_get_user(token=request.token)

		msg = actions.get_two_user_thread(auth_user, request.user)

		return msg