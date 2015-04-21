"""
Sportmate API

Module: users

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

This is a kind of super module for the api. All API.api_class calls must derive
from a single endpoints.api object. This object is held in this module.
"""

import endpoints
API = endpoints.api(name='sportmate', version='v1.0')