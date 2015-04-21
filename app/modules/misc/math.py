"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Helpful math stuff.
"""


def int_to_hex(number):
	"""
	Converts an int to a hexadecimal number. The leading '0x' and any trailing
	'L' is removed.
	"""
	return hex(number).strip("L")[2:]

def hex_to_int(string):
	"""
	Converts a hex string into an int. This function is the reverse of
	int_to_hex() such that hex_to_int(int_to_hex(987)) = 987.
	"""
	return int("0x"+ string, 0)