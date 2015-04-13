"""
Sportmate API

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

import endpoints
import logging
from protorpc import remote
from google.appengine.ext import ndb
from google.appengine.api import memcache
from misc import TextMessage
import mmglue

import actions
from messages import UserId, Relationship, FriendList, TwoUserIds, FriendRequestResponse

# Package name
API = endpoints.api(name='users', version='v1.0')

@API.api_class(resource_name='users')
class Users(remote.Service):
      
	@endpoints.method(UserId, Relationship, path='friend/request', http_method='POST', name='friendrequest')
	def friend_request(self, request):

		me = actions.verify_and_get_user(token=request.token)

		relationship = actions.friend_request(me.key.id(), request.user)

		msg = mmglue.message_from_model(relationship, Relationship)
		msg.users = [k.id() for k in relationship.users]

		return msg


	@endpoints.method(UserId, FriendList, path='friend/list', http_method='GET', name='friendlist')
	def get_friends_list(self, request):
		me = actions.verify_and_get_user(token=request.token)

		friends_list = actions.get_friends_list(request.user)

		msg = FriendList()
		msg.friends = [k.id() for k in friends_list.friends]

		return msg

	@endpoints.method(UserId, Relationship, path='friend/unfriend', http_method='POST', name='friendunfriend')
	def unfriend(self, request):
		me = actions.verify_and_get_user(token=request.token)

		relationship = actions.unfriend(me.key.id(), request.user)

		msg = mmglue.message_from_model(relationship, Relationship)
		msg.users = [k.id() for k in relationship.users]

		return msg


	@endpoints.method(TwoUserIds, Relationship, path='user/relationship', http_method='GET', name='userrelationship')
	def get_relationship(self, request):
		me = actions.verify_and_get_user(token=request.token)

		relationship = actions.get_relationship(request.userA, request.userB)

		msg = mmglue.message_from_model(relationship, Relationship)
		msg.users = [k.id() for k in relationship.users]

		return msg


	@endpoints.method(FriendRequestResponse, Relationship, path='friend/request/response', http_method='POST', name='requestresponse')
	def respond_to_friend_request(self, request):
		me = actions.verify_and_get_user(token=request.token)

		relationship = actions.respond_to_friend_request(me, request.user, request.accept)

		msg = mmglue.message_from_model(relationship, Relationship)
		msg.users = [k.id() for k in relationship.users]

		return msg