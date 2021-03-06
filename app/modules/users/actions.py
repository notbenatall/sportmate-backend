"""
Sportmate API

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file defines the actions for the user module.
"""
from endpoints import UnauthorizedException, NotFoundException
from google.appengine.ext import ndb
import modules.users.models as models
import modules.users.messages as messages
import mmglue


def verify_and_get_user(**kwargs):
	"""
	Returns the user associated with a token or raises an error.

	Params:
		token - the token that represents the validated user.
	"""

	try:
		user = models.User.get_from_token(kwargs['token'])
	except:
		raise UnauthorizedException("User is invalid.")

	if user is None:
		raise UnauthorizedException("User is invalid.")

	return user


def user_key_id_to_user(uinput):
	"""
	Takes a user or user's key or user's id as an input and returns the user.
	"""

	if type(uinput) is models.User:
		return uinput

	if hasattr(uinput, 'key') and hasattr(uinput.key, 'kind') and \
			uinput.key.kind() == "User":
		return uinput

	if type(uinput) is ndb.Key:
		user = uinput.get()
		if user is None:
			raise NotFoundException()
		return user

	if type(uinput) is long or type(uinput) is int or type(uinput) is str:
		user = models.User.get_by_id(uinput)
		if user is None:
			raise NotFoundException()
		return user

	raise TypeError("Unknown type: " + str(type(uinput)))


def user_to_message(user):
	"""
	Takes a user and returns a general user message.
	"""
	msg = mmglue.message_from_model(user, messages.User)
	return msg

def me_to_message(user):
	"""
	Takes a user and returns a user message containing their credentials.
	"""
	msg = mmglue.message_from_model(user, messages.UserMe)
	msg.token = user.get_token()
	return msg

@ndb.transactional(xg=True)
def _add_to_friends_list(user_a, user_b):
	"""Adds two users to eachother's friends list."""

	if user_a.key is None or user_b.key is None:
		raise NotFoundException("Users do not exist.")

	# TODO: Add to friends lists
	friend_list_a = models.FriendList.get_or_create_addable_friend_list(user_a)
	friend_list_a.add_friend(user_b.key)

	friend_list_b = models.FriendList.get_or_create_addable_friend_list(user_b)
	friend_list_b.add_friend(user_a.key)

	friend_list_a.put()
	friend_list_b.put()


@ndb.transactional(xg=True)
def _remove_from_friends_list(user_a, user_b):
	"""Removes two users from eachother's friends list."""

	if user_a.key is None or user_b.key is None:
		raise NotFoundException("Users do not exist.")

	users = [user_a, user_b]
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
	"""Send a friend request from a sending user to a receiving user."""

	sender = models.User.get_by_id(sender_id)
	reciever = models.User.get_by_id(receiever_id)

	if sender is None or sender.key.kind() is not "User" or \
		reciever is None or reciever.key.kind() is not "User":
		raise NotFoundException("Users do not exist.")

	# Get a relationship model in the transaction
	relationship = models.Relationship.get_by_users(sender, reciever)

	if relationship is None:
		relationship = models.Relationship.create(sender, reciever)

	# If they're already friends, just return the relationship
	if relationship.is_friends:
		return relationship

	# If the other person already sent a friend request
	if relationship.friend_request_sent and \
			relationship.friend_request_sender == reciever.key and \
			relationship.friend_request_rejected == False:
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
def respond_to_friend_request(auth_user, sender_id, accept):
	"""
	Send a response to a friend request sent by a sending user to the
	authenticating user.
	"""
	sender = models.User.get_by_id(sender_id)
	auth_user = user_key_id_to_user(auth_user)

	if sender is None or auth_user is None:
		raise NotFoundException("Users do not exist.")

	# Get a relationship model in the transaction
	relationship = models.Relationship.get_by_users(sender, auth_user)

	if relationship is None or \
			relationship.is_friends or \
			not relationship.friend_request_sent or \
			relationship.friend_request_sender == auth_user.key:
		raise NotFoundException("This person did not send a friend request.")

	if accept:
		relationship.is_friends = True
		relationship.friend_request_rejected = False
		_add_to_friends_list(auth_user, sender)
		# TODO: create notification
	else:
		relationship.friend_request_rejected = True

	relationship.put()

	return relationship

@ndb.transactional(xg=True)
def unfriend(unfriender_id, friend_id):
	"""Remove the user as a friend."""

	friend = models.User.get_by_id(friend_id)
	unfriender = models.User.get_by_id(unfriender_id)

	if friend is None or unfriender is None:
		raise NotFoundException("Users do not exist.")

	# Get a relationship model in the transaction
	relationship = models.Relationship.get_by_users(friend, unfriender)

	if relationship is None:
		relationship = models.Relationship.create(friend, unfriender)

	relationship.is_friends = False
	relationship.friend_unfriender = unfriender.key

	_remove_from_friends_list(friend, unfriender)

	relationship.put()

	return relationship


def get_relationship(user_a_, user_b_):
	"""Returns the relationship between two users."""

	user_a = user_key_id_to_user(user_a_)
	user_b = user_key_id_to_user(user_b_)

	if user_a is None or user_b is None:
		raise NotFoundException("Users do not exist.")

	relation = models.Relationship.get_by_users(user_a, user_b)

	if relation is None:
		relation = models.Relationship.create(user_a, user_b)

	return relation


def get_friends_list(user):
	"""Returns the list of friends of a user."""
	# TODO Paginate

	user = user_key_id_to_user(user)
	friendlist = models.FriendList.get_or_create_addable_friend_list(user)
	return friendlist


def user_search(term):
	"""Returns a list of users whose name starts with term."""

	term = term.lower()

	field = "searchable_name"
	gql = "SELECT * FROM User WHERE {0} >= :1 AND {0} < :2".format(field)
	query = ndb.gql(gql, term, unicode(term) + u"\ufffd")

	users = query.fetch(20)

	msg = messages.UserList()
	msg.users = [user_to_message(u) for u in users]
	return msg


def get_nearby_users(request, PAGE_SIZE=50):
	"""Returns a list of nearby users."""

	bookmark_user_created = request.bookmark_user_created

	next_result = None

	query = models.User.query().order(models.User.created_date)

	if bookmark_user_created:
		query = query.filter(models.User.created_date >= bookmark_user_created)

	users = query.fetch(PAGE_SIZE + 1)

	if len(users) == PAGE_SIZE + 1:
		next_result = users[-1]
		users = users[:PAGE_SIZE]


	msg = messages.UserList()
	msg.users = [user_to_message(u) for u in users]

	if next_result:
		msg.bookmark_user_created = next_result.created_date


	return msg



def get_user(user):
	"""
	"""
	user = user_key_id_to_user(user)
	return user_to_message(user)