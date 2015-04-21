# Copyright 2014 Adrian Letchford.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
:File: make_client_core.py
:Author: `Adrian Letchford <http://www.dradrian.com>`_
:Created On: Mon Dec 29 11:42:06 2014

Sets up the python environment for generating an Android client API 
Library from a python Google Endpoints project.

This script completely replaces the endpointscfg.py file. Follow the 
instructions on:

https://cloud.google.com/appengine/docs/python/endpoints/endpoints_tool

except you must replace the endpointscfg.py file with `python thisfile.py`. For
example, instead of calling:

google_appengine/endpointscfg.py get_client_lib java -bs gradle helloworld_api.HelloWorldApi

you would call:

python make_client_core.py get_client_lib java -bs gradle helloworld_api.HelloWorldApi

For ease, I put this command into a make_client.sh file and call:

bash make_client.sh

to make the Android client API Library.
"""

#------------------------------
# SET UP SCRIPT
#------------------------------

# Put the full file name of endpointscfg.py here
fname = "/home/adrian/Development/google_appengine/endpointscfg.py"

# Put your app's directory here
appdir = "./app"

# END SET UP SCRIPT

# Imports
import os
import sys

os.environ['MAKE_CLIENT_API'] = 'ACTIVE'

# Add the endpointscfg directory to the system path
sys.path.append(os.path.dirname(fname))

# Add your APIs directory to the system path
sys.path.append(appdir)

# Import the endpoints module
import endpointscfg

# The endpointscfg.py file defines and runs a function called run_file.
# We're going to redefine that function, inserting our evironment setup
# code.

def run_file(file_path, globals_):
  """Execute the given script with the passed-in globals.

  Args:
    file_path: the path to the wrapper for the given script. This will usually
      be a copy of this file.
    globals_: the global bindings to be used while executing the wrapped script.
  """
  script_name = os.path.basename(file_path)

  sys.path = (endpointscfg._PATHS.script_paths(script_name) +
              endpointscfg._PATHS.scrub_path(script_name, sys.path))

  if 'google' in sys.modules:
    del sys.modules['google']
    
  #------------------------------
  # SET UP YOUR ENVIRONMENT
  #------------------------------
  import appengine_config
  
  # END SET UP YOUR ENVIRONMENT
	
  execfile(endpointscfg._PATHS.script_file(script_name), globals_)


# Run the function
run_file(fname, globals())
