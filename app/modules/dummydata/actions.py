"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Dummy data functions
"""
import random
from datetime import datetime, timedelta

import modules.sports as sports
import modules.sports.models  # pylint: disable=unused-import
import modules.sports.actions
import modules.sports.messages

import modules.users as users
import modules.users.models  # pylint: disable=unused-import

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

	user_list = [
		{
			'full_name': "Adrian Letchford",
		},
		{
			'full_name': "Tom Haleminh",
		},
		{
			'full_name': "Barney",
		},
		{
			'full_name': "Joyce Chan",
		},
	]

	entities = []

	for user in user_list:
		userm = users.models.User(full_name=user['full_name'])
		userm.initialise_new_token()
		userm.put()
		entities.append(userm)

	return entities


def dummy_data_create_games(categories, user_list):
	"""Creates some dummy games for building the front end."""

	for _ in range(20):

		# Get a random cateogory
		category = random.choice(categories)

		# University of Warwick boundaries
		north = 52.391688
		south = 52.371125
		east = -1.571832
		west = -1.548099

		# Get a random user
		user = random.choice(user_list)

		# Random time
		time = datetime.now() + timedelta(seconds=random.uniform(0, 7*24*60*60))

		new_game_msg = sports.messages.NewGame(
			categories=[category.name],
			level=random.choice(range(1, 5)),
			time=time,
			name='Random name',
			players_needed=random.choice(range(1, 5)),
			lat=random.uniform(south, north),
			lon=random.uniform(east, west))

		sports.actions.create_new_game(user, new_game_msg)


def dummy_data_create():
	"""Run all the create dummy data functions."""
	categories = dummy_data_create_categories()
	user_list = dummy_data_create_users()
	dummy_data_create_games(categories, user_list)