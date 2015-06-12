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

	data = [
		{"venue": "Warwick Sports Centre", "subvenue": "Activity Room", "lat": 52.381639, "lon": -1.558609},
		{"venue": "Warwick Sports Centre", "subvenue": "Climbing Centre", "lat": 52.381639, "lon": -1.558610},
		{"venue": "Warwick Sports Centre", "subvenue": "Desso Hall", "lat": 52.381639, "lon": -1.558611},
		{"venue": "Warwick Sports Centre", "subvenue": "Functional Studio", "lat": 52.381639, "lon": -1.558612},
		{"venue": "Warwick Sports Centre", "subvenue": "Gym", "lat": 52.381639, "lon": -1.558613},
		{"venue": "Warwick Sports Centre", "subvenue": "Main Hall", "lat": 52.381639, "lon": -1.558614},
		{"venue": "Warwick Sports Centre", "subvenue": "Squash Court", "lat": 52.381639, "lon": -1.558615},
		{"venue": "Warwick Sports Centre", "subvenue": "Studio", "lat": 52.381639, "lon": -1.558616},
		{"venue": "Warwick Sports Centre", "subvenue": "Swimming Pool", "lat": 52.381639, "lon": -1.558617},
		{"venue": "Warwick Sports Centre", "subvenue": "Other", "lat": 52.381639, "lon": -1.558618},

		{"venue": "Westwood", "subvenue": "3G Tarkett Pitch", "lat": 52.386645, "lon": -1.5662780000000112},
		{"venue": "Westwood", "subvenue": "American Football Pitch", "lat": 52.390754, "lon": -1.5649960000000647},
		{"venue": "Westwood", "subvenue": "Astro Pitch", "lat": 52.389833, "lon": -1.565170999999964},
		{"venue": "Westwood", "subvenue": "Athletics Track", "lat": 52.387584, "lon": -1.565924999999993},
		{"venue": "Westwood", "subvenue": "Dance Studio", "lat": 52.389423, "lon": -1.5599569999999403},
		{"venue": "Westwood", "subvenue": "Frisbee Pitch", "lat": 52.383513, "lon": -1.5670539999999846},
		{"venue": "Westwood", "subvenue": "Games Hall", "lat": 52.386955, "lon": -1.564583999999968},
		{"venue": "Westwood", "subvenue": "Tennis Centre", "lat": 52.388227, "lon": -1.5648730000000342},
		{"venue": "Westwood", "subvenue": "Westwood", "lat": 52.388533, "lon": -1.564516},

		{"subvenue": "Cricket Pitches", "venue": "Cryfield", "lat": 52.373498, "lon": -1.5636959999999362},
		{"subvenue": "Football Pitches", "venue": "Cryfield", "lat": 52.375461, "lon": -1.5647089999999935},
		{"subvenue": "Lacrosse Pitches", "venue": "Cryfield", "lat": 52.372604, "lon": -1.5639479999999821},
		{"subvenue": "Rugby Pitches", "venue": "Cryfield", "lat": 52.37319, "lon": -1.5665689999999586},
		{"subvenue": "Cryfield", "venue": "Cryfield", "lat": 52.375897, "lon": -1.5659709999999905},

		{"venue": "Lakeside", "subvenue": "Lakeside", "lat": 52.380763, "lon": -1.57320100000004},
	]

	locations = messages.LocationCollection()

	for dic in data:
		location = messages.Location()
		location.venue = dic["venue"]
		location.subvenue = dic["subvenue"]
		location.lat = dic["lat"]
		location.lon = dic["lon"]

		locations.locations.append(location)

	return locations
