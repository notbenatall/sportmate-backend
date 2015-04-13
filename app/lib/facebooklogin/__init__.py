from urllib import urlencode, urlopen
import cgi
from datetime import datetime, timedelta
import json

class FacebookLogin(object):

	USER_LOGIN_URL = "https://graph.facebook.com/oauth/authorize?"
	GET_ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token?"

	def __init__(self, client_id, client_secret, redirect_url):
		self.client_id = client_id
		self.client_secret = client_secret
		self.redirect_url = redirect_url
		self.access_token = None
		self.expires = None

	def make_user_login_url(self):
		"""Builds the url that a user will use to login with Facebook."""
		args = dict(client_id=self.client_id, redirect_uri=self.redirect_url, scope='email')
		url = self.USER_LOGIN_URL + urlencode(args)
		return url

	def make_retrieve_access_token_url(self, code):
		"""Builds the url for retrieving the access token."""
		args = dict(client_id=self.client_id, client_secret=self.client_secret, code=code, redirect_uri=self.redirect_url)
		url = self.GET_ACCESS_TOKEN_URL + urlencode(args)		
		return url

	def _set_expires_in_seconds(self, seconds):
		self.expires = datetime.now() + timedelta(0,seconds)

 	def retrieve_access_token(self, code):
 		url = self.make_retrieve_access_token_url(code)
 		data = urlopen(url).read()

 		res = cgi.parse_qs(data)
 		if len(res) == 0:
 			raise Exception(data)

 		self.access_token = res['access_token'][-1]
 		self._set_expires_in_seconds(int(res['expires'][-1]))


 	def get_profile(self):

 		if self.access_token is None:
 			raise Exception("You must have an access token.")

 		profile = json.load(urlopen("https://graph.facebook.com/me?" + urlencode(dict(access_token=self.access_token))))

 		return profile
