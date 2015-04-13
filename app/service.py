# This starts the app.

import endpoints
import facebook.api
import users.api

APPLICATION = endpoints.api_server([users.api.API, facebook.api.API])
