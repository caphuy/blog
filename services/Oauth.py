import json

from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, g
import logging


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']
    
    def authorize(self):
        pass
    def callback(self):
        pass
    
    def get_callback_url(self):
        logging.info(request.host_url + 'user/oauth/callback/' + self.provider_name)
        return request.host_url + 'user/oauth/callback/' + self.provider_name

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider

        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id= self.consumer_id,
            client_secret = self.consumer_secret,
            authorize_url = 'https://graph.facebook.com/oauth/authorize',
            access_token_url = 'https://graph.facebook.com/oauth/access_token',
            base_url = 'https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope = 'email',
            response_type = 'code',
            redirect_uri = self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        
        logging.info(request.args);
        oauth_session = self.service.get_auth_session(
            data = {
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('me?fields=id,email').json()
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],
            me.get('email')
        )


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = OAuth2Service(
            name='google',
            client_id= self.consumer_id,
            client_secret = self.consumer_secret,
            authorize_url = 'https://accounts.google.com/o/oauth2/auth',
            access_token_url = 'https://accounts.google.com/o/oauth2/token',
            base_url = 'https://www.googleapis.com/oauth2/v1/'
        )
    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope = 'https://www.googleapis.com/auth/userinfo.email',
            response_type = 'code',
            redirect_uri = self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        
        logging.info(request.args)
        logging.info(request)
        
        oauth_session = self.service.get_auth_session(
            data = {
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        return (
            'google$' + me['id'],
            me.get('email').split('@')[0],
            me['email']
        )