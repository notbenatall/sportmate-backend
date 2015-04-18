"""
Sportmate API v1

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com

Helpful messages stuff.
"""
# pylint: disable= no-init, too-few-public-methods

from protorpc import messages

class TextMessage(messages.Message):
	"""Simple generic message for arbitrary text."""
	text = messages.StringField(1)