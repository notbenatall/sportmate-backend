# This starts the app.

import os
import endpoints
import modules.api
import modules.facebook.api
import modules.users.api
import modules.sports.api

import modules.misc as misc

if misc.is_development() or misc.is_test():
	import modules.dummydata.api

APPLICATION = endpoints.api_server([modules.api.API])