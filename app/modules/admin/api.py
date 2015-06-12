"""
Sportmate API

Module: sports.api

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

"""
# pylint: disable=no-self-use, no-init, unused-argument

from google.appengine.ext import ndb
import endpoints
from protorpc import remote

import modules.admin.actions as actions
from modules.misc.messages import VoidMessage, TextMessage

import modules.api

@modules.api.API.api_class(resource_name='admin')
class Admin(remote.Service):

	@endpoints.method(VoidMessage, TextMessage, path='admin/create_sport_categories',
		http_method='GET', name='create_sport_categories')
	def create_new_categories(self, request):
		"""Adds the sport categories to the system."""
		actions.create_sport_categories()
		return TextMessage(text="done!")