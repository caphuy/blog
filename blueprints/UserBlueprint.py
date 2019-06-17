from flask import Blueprint, redirect, url_for, jsonify, make_response
from services.Oauth import OAuthSignIn
from Model import db, User, UserSchema
import logging
import json
from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)

jwt = JWT()

user_blueprint = Blueprint('user_blueprint', __name__)
users_schema = UserSchema(many = True)
user_schema = UserSchema()

@user_blueprint.route('/authorize/<provider>')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@user_blueprint.route('/oauth/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    logging.info(social_id)
    logging.info(username)
    logging.info(email)

    #Login failed
    if social_id is None:
        return jsonify({
            'status': 'ng',
            'data': {}
        }), 401

    #Login success
    user = User.query.filter_by(email = email).first()
    user = user_schema.dump(user).data
    logging.info(user)
    logging.info(user == {})
    logging.info(user != {})

    if user == {}:
        #User not existed
        logging.info('User not existed')
        user = User(username, provider, email, None, None, None)
        logging.info(user)
        db.session.add(user)
        db.session.commit()
        user = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "social_id": user.social_id,
            "fullname": user.full_name,
            "phone_number": user.phone_number
        }
    else:
        #User existed
        logging.info('User existed')
        logging.info(user)
        if user['social_id'] == 'facebook' and provider == 'google':
            logging.info('User facebook sign in via google')
        else:
            logging.info('User facebook or google')    

    #Data token
    data_encode = {
        'iss': 'http://localhost:5000',
        'sub': 'sudo',
        'data': {
            'user_id': user['id']
        }
    }
    #Get private key
    with open('rsa_private_key.pem', 'rb') as fh:
        signing_key = jwk_from_pem(fh.read())

    #Generate token
    jwt = JWT()
    token = jwt.encode(data_encode, signing_key, 'RS256')
    logging.info(token)

    #Return response
    response = make_response(jsonify({
        'status': 'ok',
        'data': user
    }), 200)
    response.headers['token'] = token
    return response