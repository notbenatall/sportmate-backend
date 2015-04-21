# This starts the app.

import endpoints
import modules.api
import modules.facebook.api
import modules.users.api
import modules.sports.api

APPLICATION = endpoints.api_server([modules.api.API])
