# This starts the app.

import endpoints
import modules.facebook.api as facebook
import modules.users.api as users
import modules.sports.api as sports

APPLICATION = endpoints.api_server([users.API, facebook.API, sports.API])
