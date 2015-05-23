"""
Sportmate API

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable=no-self-use, no-init

import endpoints
from protorpc import remote
import mmglue

import modules.users.actions as actions
import modules.users.messages as messages

import modules.api

@modules.api.API.api_class(resource_name='users')
class Users(remote.Service):
	"""
	Access and modify information about users.
	"""
	@endpoints.method(messages.UserId, messages.Relationship,
		path='friend/request', http_method='POST', name='friendrequest')
	def friend_request(self, request):
		"""Send a friend request."""
		auth_user = actions.verify_and_get_user(token=request.token)

		relationship = actions.friend_request(auth_user.key.id(), request.user)

		msg = mmglue.message_from_model(relationship, messages.Relationship)
		msg.users = [k.id() for k in relationship.users]

		return msg

	@endpoints.method(messages.UserId, messages.FriendList, path='friend/list',
		http_method='GET', name='friendlist')
	def get_friends_list(self, request):
		"""Return a list of friends for the specified user."""
		actions.verify_and_get_user(token=request.token)

		friends_list = actions.get_friends_list(request.user)

		msg = messages.FriendList()
		msg.friends = [k.id() for k in friends_list.friends]

		return msg

	@endpoints.method(messages.UserId, messages.Relationship,
		path='friend/unfriend', http_method='POST', name='friendunfriend')
	def unfriend(self, request):
		"""
		Remove the specified user as a friend of the authenticating user.
		"""
		auth_user = actions.verify_and_get_user(token=request.token)

		relationship = actions.unfriend(auth_user.key.id(), request.user)

		msg = mmglue.message_from_model(relationship, messages.Relationship)
		msg.users = [k.id() for k in relationship.users]

		return msg


	@endpoints.method(messages.TwoUserIds, messages.Relationship,
		path='user/relationship', http_method='GET', name='userrelationship')
	def get_relationship(self, request):
		"""
		Returns the relationship between two users.
		"""
		actions.verify_and_get_user(token=request.token)

		relationship = actions.get_relationship(request.userA, request.userB)

		msg = mmglue.message_from_model(relationship, messages.Relationship)
		msg.users = [k.id() for k in relationship.users]

		return msg


	@endpoints.method(messages.FriendRequestResponse, messages.Relationship,
		path='friend/request/response', http_method='POST',
		name='requestresponse')
	def respond_to_friend_request(self, request):
		"""
		Answer a friend request from a user to the authenticating user.
		"""
		auth_user = actions.verify_and_get_user(token=request.token)

		relationship = actions.respond_to_friend_request(auth_user,
			request.user, request.accept)

		msg = mmglue.message_from_model(relationship, messages.Relationship)
		msg.users = [k.id() for k in relationship.users]

		return msg


	@endpoints.method(messages.UserId, messages.User,
		path='user', http_method='POST',
		name='getuser')
	def get_user(self, request):
		"""
		Get information about a user.
		"""
		auth_user = actions.verify_and_get_user(token=request.token)

		msg = actions.user_to_message(auth_user)

		return msg



	@endpoints.method(messages.UserSearch, messages.UserList,
		path='user/search', http_method='POST',
		name='usersearch')
	def user_search(self, request):
		"""
		Searchers for users
		"""
		actions.verify_and_get_user(token=request.token)

		msg = actions.user_search(request.term)
		return msg


	@endpoints.method(messages.UserSearch, messages.UserList,
		path='user/nearby', http_method='POST',
		name='usernearby')
	def get_nearby_users(self, request):
		"""
		Get nearby users
		"""
		actions.verify_and_get_user(token=request.token)

		msg = actions.get_nearby_users(request)
		print msg
		return msg