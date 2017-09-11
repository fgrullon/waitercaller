try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json

TOKEN = "a1a3db4bd4044d1022fdb45f1a4d18a9240eaede"
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:

	def shorten_url(self, longurl):
		try:
			url = ROOT_URL + SHORTEN.format(TOKEN, longurl)
			response = urllib2.urlopen(url).read()
			jr = json.loads(response)
			return jr['data']['url']
		except Exception as e:
			print(e)
