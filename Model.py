from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()
  
class Post(db.Model):
  __tablename__ = 'posts'
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  title = db.Column(db.String(150), nullable = False)
  intro = db.Column(db.Text, nullable = False)
  content = db.Column(db.Text, nullable = False)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
  def __init__(self, title, intro, content, user_id):
    self.title = title
    self.intro = intro
    self.content = content
    self.user_id = user_id

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  username = db.Column(db.String(150), nullable = False)
  email = db.Column(db.String(150), nullable = False)
  social_id = db.Column(db.String(150), nullable = True)
  full_name = db.Column(db.String(150), nullable = True)
  phone_number = db.Column(db.String(150), nullable = True)
  job = db.Column(db.String(150), nullable = True)
  posts = db.relationship('Post', cascade='all,delete-orphan', single_parent=True, backref=db.backref('users', lazy='joined'))
  def __init__(self, username, social_id, email, full_name, phone_number, job):
    self.username = username
    self.social_id = social_id
    self.email = email
    self.full_name = full_name
    self.phone_number = phone_number
    self.job = job

class Action(db.Model):
  __tablename__ = 'actions'
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  user_id = db.Column(db.Integer, nullable = False)
  post_id = db.Column(db.Integer, nullable = False)
  action = db.Column(db.String(30), nullable = False)
  def __init__(self, user_id, post_id, action):
    self.user_id = user_id
    self.post_id = post_id
    self.action = action

class PostSchema(ma.ModelSchema):
  id = fields.Integer(dump_only = True)
  title = fields.String(required = True)
  intro = fields.String(required = True)
  content = fields.String(required = True)
  user_id = fields.Integer(required = True)

class UserSchema(ma.Schema):
  id = fields.Integer(dump_only = True)
  username = fields.String(required = True)
  password = fields.String(required = True)
  social_id = fields.String(required = False)
  full_name = fields.String(required = False)
  phone_number = fields.String(required = False)
  job = fields.String(required = False)
  posts = fields.Nested(PostSchema, many = True)

class ActionSchema(ma.ModelSchema):
  id = fields.Integer(dump_only = True)
  user_id = fields.Integer(required = True)
  post_id = fields.Integer(required = True)
  action = fields.String(required = True)