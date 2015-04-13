"""
Sportmate API

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file defines the actions for the user module.
"""
import endpoints
from google.appengine.ext import ndb
import users.models as models


def verify_and_get_user(**kwargs):
	"""
	Returns the user associated with dumb_token or raises an error.

	Params:
		token - the token that represents the validated user.
	"""

	user = models.User.get_from_dumb_token(kwargs['token'])

	if user is None:
		raise endpoints.UnauthorizedException("User is invalid.")

	return user


def user_key_id_to_user(uinput):
	"""
	Takes a user or ueser's key or user's id as an input and returns the user.
	"""

	if type(uinput) is models.User:
		return uinput

	if type(uinput) is ndb.Key:
		user = uinput.get()
		if user is None:
			raise endpoints.NotFoundException()
		return user

	if type(uinput) is long or type(uinput) is str:
		user = models.User.get_by_id(uinput)
		if user is None:
			raise endpoints.NotFoundException()
		return user

	raise TypeError("Unknown type.")

@ndb.transactional(xg=True)
def _add_to_friends_list(userA, userB):

	if userA.key is None or userB.key is None:
		raise endpoints.NotFoundException("Users do not exist.")

	# TODO: Add to friends lists
	friend_listA = models.FriendList.get_or_create_addable_friend_list(userA)
	friend_listA.add_friend(userB.key)

	friend_listB = models.FriendList.get_or_create_addable_friend_list(userB)
	friend_listB.add_friend(userA.key)

	friend_listA.put()
	friend_listB.put()


@ndb.transactional(xg=True)
def _remove_from_friends_list(userA, userB):

	if userA.key is None or userB.key is None:
		raise endpoints.NotFoundException("Users do not exist.")

	users =[userA, userB]
	for i in range(2):
		current_user = users[i]
		friend = users[(i+1)%2] 

		query = models.FriendList.query(ancestor=current_user.key)
		friend_list = query.get()
		if friend_list is not None:
			friend_list.friends.remove(friend.key)
			friend_list.put()


@ndb.transactional(xg=True)
def friend_request(sender_id, receiever_id):

	sender = models.User.get_by_id(sender_id)
	reciever = models.User.get_by_id(receiever_id)

	if sender is None or type(sender) is not models.User or reciever is None or type(reciever) is not models.User:
		raise endpoints.NotFoundException("Users do not exist.")

	# Get a relationship model in the transaction
	relationship = models.Relationship.get_by_users(sender, reciever)

	if relationship is None:
		relationship = models.Relationship.create(sender, reciever)

	# If they're already friends, just return the relationship
	if relationship.is_friends:
		return relationship

	# If the other person already sent a friend request
	if relationship.friend_request_sent and relationship.friend_request_sender == reciever.key and relationship.friend_request_rejected == False:
		relationship.is_friends = True
		_add_to_friends_list(reciever, sender)

	else:
		relationship.friend_request_sent = True
		relationship.friend_request_sender = sender.key
		relationship.friend_request_rejected = False

	relationship.put()

	# TODO: Send notification

	return relationship

@ndb.transactional(xg=True)
def respond_to_friend_request(me, sender_id, accept):

	sender = models.User.get_by_id(sender_id)
	me = user_key_id_to_user(me)

	if sender is None or me is None:
		raise endpoints.NotFoundException("Users do not exist.")

	# Get a relationship model in the transaction
	relationship = models.Relationship.get_by_users(sender, me)

	if relationship is None or \
			relationship.is_friends or \
			not relationship.friend_request_sent or \
			relationship.friend_request_sender == me.key:
		raise endpoints.NotFoundException("This person did not send a friend request.")

	if accept:
		relationship.is_friends = True
		relationship.friend_request_rejected = False
		_add_to_friends_list(me, sender)
		# TODO: create notification
	else:
		relationship.friend_request_rejected = True

	relationship.put()

	return relationship

@ndb.transactional(xg=True)
def unfriend(me_id, sender_id):

	sender = models.User.get_by_id(sender_id)
	me = models.User.get_by_id(me_id)

	if sender is None or me is None:
		raise endpoints.NotFoundException("Users do not exist.")

	# Get a relationship model in the transaction
	relationship = models.Relationship.get_by_users(sender, me)

	if relationship is None:
		relationship = models.Relationship.create(sender, me)

	relationship.is_friends = False
	relationship.friend_unfriender = me.key

	_remove_from_friends_list(sender, me)

	relationship.put()

	return relationship


def get_relationship(userA_input, userB_input):

	userA = user_key_id_to_user(userA_input)
	userB = user_key_id_to_user(userB_input)

	if userA is None or userB is None:
		raise endpoints.NotFoundException("Users do not exist.")

	relation = models.Relationship.get_by_users(userA, userB)

	if relation is None:
		relation = models.Relationship.create(userA, userB)

	return relation


def get_friends_list(user):
	# TODO Paginate

	user = user_key_id_to_user(user)
	friendlist = models.FriendList.get_or_create_addable_friend_list(user)
	return friendlist