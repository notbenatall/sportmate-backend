# This starts the app.

import os
import endpoints
import modules.api
import modules.facebook.api
import modules.users.api
import modules.sports.api

if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Development'):
	import modules.dummydata.api

APPLICATION = endpoints.api_server([modules.api.API])
