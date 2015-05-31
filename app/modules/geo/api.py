"""
Sportmate API

Module: geo

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable=unused-argument, no-self-use

import endpoints
from protorpc import message_types
from protorpc import remote
import mmglue

import modules.geo.messages as messages
import modules.geo.actions as actions

import modules.api


@modules.api.API.api_class(resource_name='geo')
class Geo(remote.Service):
	"""Geographic tools."""

	@endpoints.method(message_types.VoidMessage, messages.LocationCollection,
		path='geo/defaultplaces', http_method='GET', name='getdefaultplaces')
	def get_default_places(self, request):
		"""
		Returns a list of venues around Warwick Campus.
		"""
		return actions.get_default_locations()