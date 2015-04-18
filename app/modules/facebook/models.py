"""
Sportmate API v1

Module: facebook

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

from google.appengine.ext import ndb
import misc # sportmate's misc module
from users.models import User



class FacebookAccount(ndb.Model):
	"""
	Defines a Facebook account with credentials.

	Parent: User

	Fields:
		tokensecret - A single index of both the token and secret. This enables
			us to search by token and secret without requiring two separate
			indexes.
	"""

	# Parent = User
	facebook_id = ndb.IntegerProperty(indexed=True, required=True)
	access_token = ndb.StringProperty(indexed=True, required=True)
	expires = ndb.DateTimeProperty(indexed=False, required=False)

	def validate(self):
		"""Validates this model."""
		misc.validate_parent(self, User)

	def put(self):
		"""Overrides the default put() behaviour to setup automatic fields."""
		self.validate()
		super(FacebookAccount, self).put()

	@staticmethod
	def get_by_facebook_id(facebook_id):
		"""Returns a FacebookAccount from a Facebook user ID."""
		query = FacebookAccount.query(
			FacebookAccount.facebook_id == long(facebook_id))
		account = query.get()
		return account    