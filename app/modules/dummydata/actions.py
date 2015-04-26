"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Dummy data functions
"""
# pylint: disable=protected-access
import random
from datetime import datetime, timedelta

import modules.sports as sports
import modules.sports.models  # pylint: disable=unused-import
import modules.sports.actions
import modules.sports.messages

import modules.facebook.actions as fbactions

def dummy_data_create_categories():
	"""Creates some dummy cateogories for building the front end."""

	categories = [
		('Ball Games', []),
		('Racket Games', []),
		('Basket Ball', ['Ball Games']),
		('Tennis', ['Ball Games', 'Racket Games']),
		('Football', ['Ball Games']),
		('Badminton', ['Racket Games']),
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
			'id': 662369520,
			'email': 'someone@someplace.com',
		},
		{
			'name': "Tom Haleminh",
			'id': 1539027955,
			'email': 'someone@someplace.com',
		},
		{
			'name': "Barney Yau",
			'id': 597975737,
			'email': 'someone@someplace.com',
		},
		{
			'name': "Joyce Chan",
			'id': 679300985,
			'email': 'someone@someplace.com',
		},
	]

	entities = []

	for profile in profiles:

		fb_account = fbactions._create_new_user(profile, 'some_access_token')
		userm = fb_account.key.parent().get()
		entities.append(userm)

	return entities


def dummy_data_create_games(categories, user_list):
	"""Creates some dummy games for building the front end."""

	for _ in range(20):

		# Get a random cateogory
		category = random.choice([cat for cat in categories if len(cat.paths) > 0])

		# University of Warwick boundaries
		north = 52.391688
		south = 52.371125
		east = -1.571832
		west = -1.548099

		# Get a random user
		user = random.choice(user_list)

		# Random time
		time = datetime.now() + timedelta(seconds=random.uniform(0, 7*24*60*60))
		end_time = time + timedelta(seconds=random.uniform(1*60*60, 3*60*60))

		new_game_msg = sports.messages.NewGame(
			categories=[category.name],
			level=random.choice(range(1, 5)),
			time=time,
			end_time=end_time,
			name='Random name',
			players_needed=random.choice(range(2, 5)),
			lat=random.uniform(south, north),
			lon=random.uniform(east, west))

		#if random.randint(0, 1):
		new_game_msg.location_name = "University of Warwick"

		sports.actions.create_new_game(user, new_game_msg)


def dummy_data_create():
	"""Run all the create dummy data functions."""
	categories = dummy_data_create_categories()
	user_list = dummy_data_create_users()
	dummy_data_create_games(categories, user_list)