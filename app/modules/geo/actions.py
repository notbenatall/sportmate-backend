"""
Sportmate API

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

import modules.geo.messages as messages


def get_default_locations():
	"""
	Returns a list of venues around Warwick Campus.
	"""

	venues = {
		"w_spts_cntre": {"venue": "Warwick Sports Centre", "lat": 89.0, "lon": 856.98},
	}

	data = [
		{"venue_id": "w_spts_cntre", "subvenue": "Squash court 1"},
		{"venue_id": "w_spts_cntre", "subvenue": "Squash court 2"},
	]

	locations = messages.LocationCollection()

	for dic in data:
		location = messages.Location()
		location.venue = venues[dic["venue_id"]]["venue"]
		location.subvenue = dic["subvenue"]
		location.lat = venues[dic["venue_id"]]["lat"]
		location.lon = venues[dic["venue_id"]]["lon"]

		locations.locations.append(location)

	return locations
