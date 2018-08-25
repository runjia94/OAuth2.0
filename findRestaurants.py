from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "IJMW3YVR2PDOOROFNJ4KSHYE4RMFTS4HDYKOCVFFQPIU5ZMF"
foursquare_client_secret = "PI43YCQUKSZTJSPKCXIYEFAVHXOTEORNZK3CNVHJIVFJYV0T"


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
	latitude,longitude = getGeocodeLocation(location)
	url = (
		'https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20180824&ll=%s,%s&query=%s' % (
			foursquare_client_id,foursquare_client_secret,latitude,longitude,mealType)) 
	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
	h = httplib2.Http()
	response, content = h.request(url,'GET')
	result = json.loads(content)
	#3. Grab the first restaurant
	if result['response']['venues']:
		restaurant = result['response']['venues'][0]
		venue_id = restaurant['id']
		restaurant_name = restaurant['name']
		restaurant_address = restaurant['location']['formattedAddress']
		address = ''
		for i in restaurant_address:
			address = address + i + ' '
		restaurant_address = address

	

	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
		imageurl = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20180824' % (
				venue_id, foursquare_client_id, foursquare_client_secret))
		imgresponse,imgcontent = h.request(imageurl,'GET')
		imgresult = json.loads(imgcontent)
		#5. Grab the first image
		if imgresult['response']['photos']['items']:
			firstimg = imgresult['response']['photos']['items'][0]
			prefix = firstimg['prefix']
			suffix = firstimg['suffix']
			imgurl = prefix + '300*300' + suffix
		else:
			#6. If no image is available, insert default a image url
			imgurl = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
		restaurantinfo = {'name':restaurant_name, 'address':restaurant_address,'img':imgurl}
		print 'Restaurant Name: %s' % restaurantinfo['name']
		print 'Restaurant Address: %s' % restaurantinfo['address'] 
		print 'Image: \n %s \n' % restaurantinfo['img']
		return restaurantinfo
	
	#7. Return a dictionary containing the restaurant name, address, and image url	

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")