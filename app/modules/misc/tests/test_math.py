import sys
import nose
from nose.tools import *
from nose.plugins.attrib import attr
import logging
from datetime import datetime

import modules.misc.math as math



def test_convert_to_and_from_1():
	assert math.hex_to_int(math.int_to_hex(123456789)) == 123456789