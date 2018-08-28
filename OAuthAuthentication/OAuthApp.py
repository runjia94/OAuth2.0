from models import Base, User
from flask import Flask, jsonify, request, url_for, abort, g,render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

auth = HTTPBasicAuth()


engine = create_engine('sqlite:///userWithOAuth.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(
	open('client_secrets.json','r').read())['web']['client_id']

@auth.verify_password
def verify_password(username_or_token,password):
	#try to see if it is a token first
	user_id = User.verify_auth_token(username_or_token)
	if user_id:
		user = session.query(User).filter_by(id = user_id).first()
	else:
		user = session.query(User).filter_by(username = username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True
@app.route('/clientOAuth')
def start():
	return render_template('clientOAuth.html')

@app.route('/oauth/<provider>', methods = ['POST'])
def login(provider):
	#step1 Parse the auth code
	auth_code = request.json.get('auth_code')
	print 'Complete, received auth code %s' % auth_code
	if provider == 'google':
		#step2 exchange for a token
		try:
			#update the authorization code into a credential object
			oauth_flow = flow_from_clientsecrets('client_secrets.json',scope = '')
			oauth_flow.redirect_url = 'postmessage'
			credentials = oauth_flow.step2_exchange(auth_code)
		except FlowExchangeError:
			response = make_response(json.dumps('Failed to upgrade the authorization code'),401)
			response.headers['Content-Type'] = 'application/json'
			return response
		#check that the access token is valid
		access_token = credentials.access_token
		url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
		h = httplib2.Http()
		result = json.loads(h.request(url,'GET')[1])
		#if token has error, abort
		if result.get('error') is not None:
			response = make_response(json.dumps(result.get('error')),500)
			response.headers['Content-Type'] = 'application/json'
		print 'Step2 Complete! Access Token: %s' % credentials.access_token

		#step3 Find user or make a new one
		#Get user info
		h = httplib2.Http()
		userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
		params = {'access_token': credentials.access_token, 'alt':'json'}
		answer = requests.get(userinfo_url,params = params)
		data = answer.json()

		name = data['name']
		picture = data['picture']
		email = data['email']

		user = session.query(User).filter_by(email = email).first()
		if not user:
			user = User(username = username, picture = picture, email = email)
			session.add(user)
			session.commit()

		#STEP4 Make token
		token = user.generate_auth_token(600)

		#step5 send back token to client

		return jsonify({'token':token.decode('ascii')})
	else:
		return 'Unrecoginized Provider'









@app.route('/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({'token':token.decode('ascii')})


@app.route('/users', methods = ['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')

	if username is None or password is None:
		print "Missing Arguments"
		abort(400)
	if session.query(User).filter_by(username = username).first() is not None:
		print "Existing user"
		user = session.query(User).filter_by(username=username).first()
		return jsonify({'message':'user already exists'}),200


	user = User(username = username)
	user.hash_password(password)
	session.add(user)
	session.commit()
	return jsonify({'username': user.username}),201#,{'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
	user = session.query(User).filter_by(id = id).one()
	if not user:
		abort(400)
	return jsonify({'username': user.username})

@app.route('/api/resource')
@auth.login_required
def get_resource():
	return jsonify({'data': 'Hello, %s !'% g.user.username})

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port = 5000)