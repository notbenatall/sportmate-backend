"""
Sportmate API

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

from protorpc import messages
from protorpc import message_types


class User(messages.Message):
	full_name = messages.StringField(1)
	email = messages.StringField(2)
	id = messages.IntegerField(3)

class UserMe(messages.Message):
	full_name = messages.StringField(1)
	dumb_token = messages.StringField(2)
	email = messages.StringField(3)
	id = messages.IntegerField(4)

class UserId(messages.Message):
	token = messages.StringField(1)
	user = messages.IntegerField(2)

class TwoUserIds(messages.Message):
	token = messages.StringField(1)
	userA = messages.IntegerField(2)
	userB = messages.IntegerField(3)

class FriendRequestResponse(messages.Message):
	token = messages.StringField(1)
	user = messages.IntegerField(2)
	accept =messages.BooleanField(3)



class Relationship(messages.Message):
    
    users = messages.IntegerField(1, repeated=True)
    is_friends = messages.BooleanField(2)

    friend_request_sent = messages.BooleanField(3)
    friend_request_sender_id = messages.IntegerField(4)
    friend_request_rejected = messages.BooleanField(5)
    friend_unfriender_id = messages.IntegerField(6)


class FriendList(messages.Message):
 	friends = messages.IntegerField(1, repeated=True)