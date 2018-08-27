import httplib2
import json

def getGeocodeLocation(inputString):
	google_api_key = "AIzaSyDKvHGszR_8CWmxLpWKYMhwfrK9H7Yp4zs"
	locationString = inputString.replace(" ","+")
	url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' %(locationString, google_api_key))
	h = httplib2.Http()
	#create a http instance
	response, content = h.request(url,'GET')
	result = json.loads(content)
	latitude = result['results'][0]['geometry']['location']['lat']
	longitude = result['results'][0]['geometry']['location']['lng']
	return (latitude,longitude)
