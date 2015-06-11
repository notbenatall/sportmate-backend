"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Dummy data functions
"""
# pylint: disable=protected-access, too-many-locals, invalid-name
import random
from datetime import datetime, timedelta

from google.appengine.ext import ndb

import modules.sports as sports
import modules.sports.models  # pylint: disable=unused-import
import modules.sports.actions
import modules.sports.messages

import modules.misc as misc

import modules.facebook.actions as fbactions

def dummy_data_create_categories():
	"""Creates some dummy cateogories for building the front end."""

	categories = [
		('Basketball', []),
		('Tennis', []),
		('Football', []),
		('Badminton', []),
		('Unicyling', []),
	]

	entities = []

	for category, parents in categories:

		cat = sports.models.SportCategory(name=category)
		for parent in parents:
			cat.add_parent(sports.models.SportCategory.get_by_name(parent))

		cat.put()

		entities.append(cat)

	return entities


def dummy_data_create_users():
	"""Creates some dummy users for building the front end."""

	profiles = [
		{
			'name': "Adrian Letchford",
			'first_name': "Adrian",
			'id': 10153194089974521,
			'email': 'someone@someplace.com',
		},
		{
			'name': "Tom Haleminh",
			'first_name': "Tom",
			'id': 1539027955,
			'email': 'someone@someplace.com',
		},
		{
			'name': "Barney Yau",
			'first_name': "Barney",
			'id': 597975737,
			'email': 'someone@someplace.com',
		},
		{
			'name': "Joyce Chan",
			'first_name': "Joyce",
			'id': 679300985,
			'email': 'someone@someplace.com',
		},
		{
			'name': "Catalin Craciun",
			'first_name': "Catalin",
			'id': 915399228520705,
			'email': 'catalincraciun7@yahoo.com',
		},
	]

	entities = []

	for profile in profiles:

		fb_account = fbactions._create_new_user(profile, 'some_access_token')
		userm = fb_account.key.parent().get()
		entities.append(userm)

	return entities


def dummy_data_create_sport_profiles(categories, user_list):
	"""Creates some dummy sport profiles for building the front end."""

	for user in user_list:
		msg = sports.messages.SportProfileRequest(
			sport_category_id=categories[0].key.id(),
			level=0)
		sports.actions.add_sport_profile(user, msg)

def dummy_data_create_games(categories, user_list):
	"""Creates some dummy games for building the front end."""

	for _ in range(20):

		# Get a random cateogory
		#category = random.choice([cat for cat in categories if len(cat.paths) > 0])
		category = random.choice([cat for cat in categories])

		# University of Warwick boundaries
		north = 52.391688
		south = 52.371125
		east = -1.571832
		west = -1.548099

		# Get a random user
		user = random.choice(user_list)

		# Get a random player
		#available_players = [u for u in user_list if u != user]
		#player = random.choice(available_players)

		# Random time
		one_hour = 60*60
		one_day = 24*one_hour
		start = timedelta(seconds=random.uniform(2*one_day, 7*one_day))
		duration = timedelta(seconds=random.uniform(1*one_hour, 3*one_hour))
		time = datetime.now() + start
		end_time = time + duration

		new_game_msg = sports.messages.NewGame(
			categories=[category.name],
			level=random.choice(range(1, 5)),
			time=time,
			end_time=end_time,
			name= category.name + ' at Warwick',
			players_needed=random.choice(range(3, 6)),
			lat=random.uniform(south, north),
			lon=random.uniform(east, west))

		new_game_msg.location_name = "University of Warwick"

		game = sports.actions.create_new_game(user, new_game_msg) # pylint: disable=unused-variable

		#sports.actions.join_game(player, game)


def clear_database():
	"""Clears the entire datastore."""
	ndb.delete_multi(ndb.Query().fetch(keys_only=True))


def dummy_data_create():
	"""Run all the create dummy data functions."""
	if misc.is_development_testing() or misc.is_development():
		clear_database()
	categories = dummy_data_create_categories()
	user_list = dummy_data_create_users()
	dummy_data_create_games(categories, user_list)