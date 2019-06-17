from flask import Flask
import logging
from services.Oauth import OAuthSignIn

logging.basicConfig(level=logging.DEBUG)

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from blueprints.UserBlueprint import user_blueprint
    from blueprints.PostBlueprint import post_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(post_blueprint, url_prefix='/api')

    from Model import db
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True) 