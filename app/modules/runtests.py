import sys
import os
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging

# Turn off logging. Google App Engine spits out all kinds of junk which we
# don't need.
logger = logging.getLogger()
logger.disabled = True

# Allow access to the GAE modules
sys.path.append('/home/adrian/Development/google_appengine')
sys.path.append('/home/adrian/Development/google_appengine/lib/endpoints-1.0')
sys.path.append('/home/adrian/Development/google_appengine/lib/protorpc-1.0')

# Allow access to the modules made available to this app
sys.path.append('../lib')
sys.path.append('../include')
sys.path.append('../modules')

if __name__ == '__main__':
    # Run all the tests in this file
    module_name = os.path.dirname(sys.modules[__name__].__file__)

    argv = [sys.argv[0], module_name, '--nocapture'] + sys.argv[1:]
    result = nose.run(argv=argv)
    #result = nose.run(argv=[sys.argv[0], module_name, '-v', "-a !slow"])
    #result = nose.run(argv=[sys.argv[0], module_name, '-v', "-a slow"])