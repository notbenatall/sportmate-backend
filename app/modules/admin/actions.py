"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

from modules.sports.actions import create_sport_category

def create_sport_categories():
	names = [
		'Football',
		'Cricket', 
		'Basketball', 
		'Baseball', 
		'Volleyball', 
		'Tennis', 
		'Field Hockey', 
		'American Football', 
		'Table Tennis',
		'Golf', 
		'Rugby',
		'Badminton', 
		'Fitness', 
		'Combat Sports', 
		'Rowing',
		'Gymnastics', 
		'Handball', 
		'Bowling', 
		'Swimming', 
		'Board Sports', 
		'Lacrosse', 
		'Squash', 
		'Water Sports', 
		'Other', 
		'Yoga',
		"Rock Climbing",
		"Running",
		"Frisbee"]


	for name in names:
		create_sport_category(name)
