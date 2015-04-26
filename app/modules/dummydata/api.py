"""
Sportmate API

Module: sports.api

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Holds the endpoints for the dummy data module.
"""
# pylint: disable=no-self-use, no-init, unused-argument, too-few-public-methods

import endpoints
from protorpc import remote
#import mmglue

from modules.misc.messages import TextMessage, VoidMessage
#from modules.users.actions import verify_and_get_user
import modules.dummydata.actions as actions

import modules.api

@modules.api.API.api_class(resource_name='dummydata')
class DummyData(remote.Service):
	"""
	Access and Modify information concerning dummy data.
	"""

	@endpoints.method(VoidMessage, TextMessage, path='dummydata',
		http_method='POST', name='createdummydata')
	def create_dummy_data(self, request):
		"""Adds a new game to the system."""

		actions.dummy_data_create()

		return TextMessage(text="Done!")

