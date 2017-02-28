from flask import Flask
from flask_mongoengine import MongoEngine
import os
from flask_mail import Mail
#from jinja2 import Environment

# app.config['MONGO_URI'] = 'mongodb://localhost:27017/afranky'
dbm = MongoEngine()
mail = Mail()


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config['SECRET_KEY'] = os.urandom(24)
    dbm.init_app(app)
    mail.init_app(app)

    from accounts.acc_actions import accounts_prj
    from posts.post_actions import posts_prj

    app.register_blueprint(accounts_prj)
    app.register_blueprint(posts_prj)

    return app
