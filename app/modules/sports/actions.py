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

def get_all_categories():

	categories = models.SportCategory.get_all()

	everything = messages.AllCategories()

	for cat in categories:
		cat_msg = mmglue.message_from_model(cat, messages.SportCategory)
		cat_msg.parent_ids = [parent_key.id() for parent_key in cat.parents]
		everything.categories.append(cat_msg)

	return everything

# Create a game

# Modify a game

# Join a game

# List games (with filters)

# Add sport profile

# Get sport profile(s) of a user

# Get games made by a user