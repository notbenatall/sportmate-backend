"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This file holds all the actions for the backend system. The system runs on 
Google App Engine using the NoSQL DataStore for scalability.
"""

import endpoints
import sports.models as models
import sports.messages as messages
import mmglue

def get_all_sports():

	sports = models.Sport.get_all()
	categories = models.SportCategories.get_all()

	sports.sort(key=lambda x: x.name)
	categories.sort(key=lambda x: x.name)

	everything = messages.AllSports
	everything.categories = [mmglue.message_from_model(cat, messages.SportCategory) for cat in categories]

	for sport in sports:
		for i, cat in enumerate(categories):
			if sports.key.parent() == cat.key:
				everything.categories[i].sports.append(mmglue.message_from_model(sport, messages.Sport))

	return everything

# Create a game

# Modify a game

# Join a game

# List games (with filters)

# Add sport profile

# Get sport profile(s) of a user

# Get games made by a user