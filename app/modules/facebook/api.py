"""
Sportmate API

Module: facebook

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
# pylint: disable=unused-argument, no-self-use

import endpoints
from protorpc import message_types
from protorpc import remote
import mmglue

import modules.facebook.messages as fbmsgs
import modules.users.messages as usrmessages
import modules.facebook.actions as actions

import modules.api

REDIRECT_URL = "http://127.0.0.1:8080/_ah/api/sportmate/v1.0/code"

@modules.api.API.api_class(resource_name='facebook.login')
class FacebookLogin(remote.Service):
	"""Login in with Facebook."""

	@endpoints.method(message_types.VoidMessage, fbmsgs.Url,
		path='geturl', http_method='GET', name='geturl')
	def get_login_url(self, request):
		"""Returns the Facebook login URL."""
		return fbmsgs.Url(url=actions.get_login_url(REDIRECT_URL))

	@endpoints.method(fbmsgs.Code, fbmsgs.FacebookAccountWithUser,
		path='code', http_method='GET')
	def recieve_code(self, request):
		"""Uses the login code provided by Facebook and logs in the user."""

		account = actions.grant_user_access_from_code(REDIRECT_URL, code=request.code)
		user = account.key.parent().get()

		return_msg = mmglue.message_from_model(account,
			fbmsgs.FacebookAccountWithUser)
		return_msg.user = mmglue.message_from_model(user, usrmessages.UserMe)
		return_msg.user.token = user.get_token()

		return return_msg