"""
`appengine_config.py` is automatically loaded when Google App Engine
starts a new instance of your application. This runs before any
WSGI applications specified in app.yaml are loaded.
"""

from google.appengine.ext import vendor
import os

# Third-party libraries are stored in "lib", vendoring will make
# sure that they are importable by the application.
vendor.add('lib')
vendor.add('include')
vendor.add('modules')

# This allows us to use the requests package on the development server!
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Development'):
	
    from google.appengine.tools.devappserver2.python import sandbox
    sandbox._WHITE_LIST_C_MODULES += ['_ssl', '_socket']

    import copy_of_socket as patched_socket
    import sys

    sys.modules['socket'] = patched_socket
    socket = patched_socket