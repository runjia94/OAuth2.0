from findRestaurants import findARestaurant
from restaurantmodels import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

google_api_key = "AIzaSyDKvHGszR_8CWmxLpWKYMhwfrK9H7Yp4zs"
foursquare_client_id = "IJMW3YVR2PDOOROFNJ4KSHYE4RMFTS4HDYKOCVFFQPIU5ZMF"
foursquare_client_secret = "PI43YCQUKSZTJSPKCXIYEFAVHXOTEORNZK3CNVHJIVFJYV0T"

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()
app = Flask(__name__)

@app.route("/restaurants", methods = ['GET','POST'])
def all_restaurants_handler():
	if request.method == 'GET':
		restaurants = session.query(Restaurant).all()
		return jsonify(restaurants = [i.serialize for i in restaurants])

	elif request.method == 'POST':
		mealType = request.args.get('mealType','')
		location = request.args.get('location','')
		restaurant_info = findARestaurant(mealType,location)
		if restaurant_info != "No Restaurant Found":
			restaurant = Restaurant(
				restaurant_name = unicode(restaurant_info['name']),
				restaurant_address = unicode(restaurant_info['address']),
				restaurant_image = restaurant_info['image'])
			session.add(restaurant)
			session.commit()
			return jsonify(restaurant = restaurant.serialize)
		else:
			return jsonify({"error":"No Restaurant Found for %s in %s" % (mealType,location)})

@app.route('/restaurants/<int:id>', methods = ['GET','PUT','DELETE'])
def restaurant_handler(id):
	restaurant = session.query(Restaurant).filter_by(id = id).one()
	if request.method == 'GET':
		return jsonify(restaurant = restaurant.serialize)
	elif request.method == 'PUT':
		name = request.args.get('name')
		address = request.args.get('address')
		image = request.args.get('image')
		if name:
			restaurant.restaurant_name = name
		if address:
			restaurant.restaurant_address = address
		if image:
			restaurant.restaurant_image = image
		session.commit()
		return jsonify(restaurant = restaurant.serialize)

	elif request.method == 'DELETE':
		session.delete(restaurant)
		session.commit()
		return "Restaurant Delete"



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0',port = 5000)