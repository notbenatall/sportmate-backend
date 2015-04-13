"""
Sportmate API

Module: facebook

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""

import endpoints
import logging
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import ndb
from google.appengine.api import memcache
import mmglue

from misc import TextMessage
import messages as fbmsgs
import users.messages as usrmessages
import actions

REDIRECT_URL = "http://127.0.0.1:8080/_ah/api/facebook/v1.0/code"

API = endpoints.api(name='facebook', version='v1.0')

@API.api_class(resource_name='login')
class FacebookLogin(remote.Service):

    @endpoints.method(message_types.VoidMessage, fbmsgs.UrlMessage, path='geturl', http_method='GET', name='geturl')
    def get_login_url(self, request):
    	return fbmsgs.UrlMessage(url = actions.get_login_url(REDIRECT_URL))

    @endpoints.method(fbmsgs.CodeMessage, fbmsgs.FacebookAccountWithUser, path='code', http_method='GET')
    def recieve_code(self, request):

    	account = actions.grant_user_access_from_code(REDIRECT_URL, code=request.code)
    	user = account.key.parent().get()

    	return_msg = mmglue.message_from_model(account, fbmsgs.FacebookAccountWithUser)
    	return_msg.user = mmglue.message_from_model(user, usrmessages.UserMe)

    	return return_msg