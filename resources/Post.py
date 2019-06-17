from flask import Blueprint, redirect, url_for, jsonify, make_response, request
from flask_restful import Resource
from Model import db, Post, PostSchema, Action, ActionSchema
from middlewares.LoginMiddleware import login_required
import logging

posts_schema = PostSchema(many = True)
post_schema = PostSchema()
actions_schema = ActionSchema(many = True)
action_schema = ActionSchema()

class PostResource(Resource):
    @login_required
    def post(self):
        logging.info(request.user)
        try:
            json_params = request.get_json()
            title = json_params['title']
            content = json_params['content']
            intro = content

            #Intro = 80 first character of content
            if len(content) > 80:
                intro = content[0, 80]
            
            logging.info(title)
            logging.info(content)
            logging.info(intro)

            #save
            post = Post(title, intro, content, request.user['id'])
            db.session.add(post)
            db.session.commit()
        except:
            response = make_response(jsonify({
                'status': 'ng',
                'data': {}
            }), 500)
            return response
        response = make_response(jsonify({
            'status': 'ok',
            'data': {}
        }), 201)
        return response

    @login_required
    def get(self):
        args = request.args
        result = db.engine.execute("SELECT p.id AS pid, title, intro, content, u.id AS uid, u.username AS username, (SELECT COUNT(*) FROM users AS u JOIN actions AS a ON u.id = a.user_id WHERE p.id = a.post_id) like_count, p.user_id FROM posts AS p JOIN users AS u ON u.id = p.user_id;")
        data = []
        for row in result:
            data.append({
                'id': row[0],
                'title': row[1],
                'intro': row[2],
                'content': row[3],
                'author': {
                    'id': row[4],
                    'username': row[5]
                },
                'like_count': row[6]
            })
        response = make_response(jsonify({
            'status': 'ok',
            'data': data
        }), 200)
        return response

class PostResourceWithPathVariable(Resource):
    @login_required
    def get(self, post_id):
        logging.info(request.user)

        post = Post.query.filter_by(id = post_id).first()
        post = post_schema.dump(post).data

        response = make_response(jsonify({
            'status': 'ok',
            'data': post
        }), 200)
        return response

class ActionResoureWithPathVariable(Resource):
    @login_required
    def post(self, post_id):
        logging.info(request.user)

        post = Post.query.filter_by(id = post_id).first()
        post = post_schema.dump(post).data

        logging.info(post)
        if post == {} or post['user_id'] == request.user['id']:
            response = make_response(jsonify({
                'status': 'ng',
                'data': {}
            }), 400)
            return response

        json_params = request.get_json()
        #action = 1 => like
        #action = 0 => unlike
        user_action = json_params['action']
        if user_action == 0:
            #delete
            db.session.query(Action).filter(Action.post_id == post_id).delete(synchronize_session = False)
        else:
            #save
            action = Action(request.user['id'], post_id, 'like')
            db.session.add(action)
            db.session.commit()
        
        #Return response
        response = make_response(jsonify({
            'status': 'ok',
            'data': {}
        }), 200)
        return response