"""
Sportmate API

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable= no-init, too-few-public-methods
# I don't want to know about using 'id' as a class name here.
# pylint: disable= invalid-name

from protorpc import messages

class User(messages.Message):
	"""Message containing a user."""
	full_name = messages.StringField(1)
	email = messages.StringField(2)
	id = messages.IntegerField(3)
	facebook_id = messages.IntegerField(4, required=False)
	first_name = messages.StringField(5)

class UserMe(messages.Message):
	"""Message containing the authenticated user."""
	full_name = messages.StringField(1)
	email = messages.StringField(2)
	id = messages.IntegerField(3)
	token = messages.StringField(4)
	facebook_id = messages.IntegerField(5, required=False)
	first_name = messages.StringField(6)


class UserList(messages.Message):
	"""Message containing a list of users."""
	users = messages.MessageField(User, 1, repeated=True)

class AuthUser(messages.Message):
	"""
	Message identifying the authenticating user.
	"""
	token = messages.StringField(1)

class UserId(messages.Message):
	"""
	Message from an authenticated user requesting information about another
	user.
	"""

	token = messages.StringField(1)
	user = messages.IntegerField(2)

class TwoUserIds(messages.Message):
	"""
	Message from an authenticated user requesting information about two users.
	"""
	token = messages.StringField(1)
	userA = messages.IntegerField(2)
	userB = messages.IntegerField(3)

class FriendRequestResponse(messages.Message):
	"""
	Message from an authenicated user responding to a friend request.
	"""
	token = messages.StringField(1)
	user = messages.IntegerField(2)
	accept = messages.BooleanField(3)



class Relationship(messages.Message):
	"""
	Message about a relationship between two users.
	"""
	users = messages.IntegerField(1, repeated=True)
	is_friends = messages.BooleanField(2)

	friend_request_sent = messages.BooleanField(3)
	friend_request_sender_id = messages.IntegerField(4)
	friend_request_rejected = messages.BooleanField(5)
	friend_unfriender_id = messages.IntegerField(6)


class FriendList(messages.Message):
	"""
	Message containing a user's list of friends.
	"""
	friends = messages.IntegerField(1, repeated=True)


class UserSearch(messages.Message):
	"""
	Request message to search for users by name.
	"""
	token = messages.StringField(1)
	term = messages.StringField(2)