"""
Sportmate API v1

Module: facebook

Author: Dr. Adrian Letchford
Author URL: http:www.DrAdrian.com
"""
import endpoints
from facebooklogin import FacebookLogin
import models
import users.models

FACEBOOK_APP_ID = '1581671678743146'
FACEBOOK_APP_SECRET = 'a6202756c8e6174ec30d3956ea4a76c9'

def get_login_url(redirect_url):
	login = FacebookLogin(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, redirect_url)
	login_url = login.make_user_login_url()
	return login_url

def _create_new_user(profile, access_token):

	user = users.models.User(
		full_name = profile['name'],
		email = profile['email'])
	user.initialise_new_token()
	user.put()

	account = models.FacebookAccount(
		facebook_id = long(profile['id']),
		access_token = access_token,
		parent = user.key)

	if 'expires' in profile:
		account.expires = profile['expires']
		
	account.put()

	return account

def grant_user_access_from_code(redirect_url, **kwargs):
	""" Untested code. """

	code = kwargs['code']

	login = FacebookLogin(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, redirect_url)

	try:
		login.retrieve_access_token(code)
	except:
		raise endpoints.UnauthorizedException("Unorthorised access to Facebook.")

	profile = login.get_profile()

	print profile

	account = models.FacebookAccount.get_by_facebook_id(profile['id'])

	if account is None:
		account = _create_new_user(profile, login.access_token)

	return account