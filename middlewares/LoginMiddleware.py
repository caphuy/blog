from functools import wraps
from flask import g, request, redirect, url_for, make_response, jsonify
import json
import logging
from Model import db, User, UserSchema

from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)

users_schema = UserSchema(many = True)
user_schema = UserSchema()

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = request.headers.get('token')

		responseUnauthorized = make_response(jsonify({
			'status': 'ng',
			'data': {}
		}), 401)
		if token == None:
			#Return unauthorize response
			return responseUnauthorized

		try:
			with open('rsa_public_key.pem', 'rb') as fh:
				verifying_key = jwk_from_pem(fh.read())

			jwt = JWT()
			data = jwt.decode(token, verifying_key)
			logging.info(data)
			user_id = data['data']['user_id']
			
			user = User.query.filter_by(id = user_id).first()
			user = user_schema.dump(user).data

			if user == {}:
				return responseUnauthorized
			request.user = user
		except:
			#Return unauthorize response
			return responseUnauthorized

		return f(*args, **kwargs)
	
	return decorated_function