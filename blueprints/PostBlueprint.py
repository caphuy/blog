from flask import Blueprint, redirect, url_for, jsonify, make_response
# from Model import db, Post, PostSchema
from resources.Post import PostResource, PostResourceWithPathVariable, ActionResoureWithPathVariable
from flask_restful import Api
import logging

post_blueprint = Blueprint('post_blueprint', __name__)
post_api = Api(post_blueprint)

post_api.add_resource(PostResource, '/post')
post_api.add_resource(PostResourceWithPathVariable, '/post/<string:post_id>')
post_api.add_resource(ActionResoureWithPathVariable, '/action/<string:post_id>')