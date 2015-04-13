import Geohash


class TestGeohash:

	def setup(self):
		self.family = [-35.128784, 147.320091]
		self.next_door = [-35.128967, 147.320100]
		self.sturt_mall = [-35.113545, 147.370189]
		self.the_rock = [-35.268565, 147.114741]

	def test_basic(self):

		hash = Geohash.encode(self.family[0], self.family[1], precision=20)

		(lats, lons) = Geohash.decode(hash)

		assert float(lats) == self.family[0]
		assert float(lons) == self.family[1]


	def test_proximity(self):

		famhash = Geohash.encode(self.family[0], self.family[1], precision=20)
		nexthash = Geohash.encode(self.next_door[0], self.next_door[1], precision=20)
		sturthash = Geohash.encode(self.sturt_mall[0], self.sturt_mall[1], precision=20)
		rockhash = Geohash.encode(self.the_rock[0], self.the_rock[1], precision=20)

		assert famhash[:5] == nexthash[:5]
		assert famhash[:4] == sturthash[:4]
		assert famhash[:2] == rockhash[:2]
