# from app.v1.models.db_connect import db

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
import os, binascii

from instance.config import app_config

app = FlaskAPI(__name__, instance_relative_config=True)

secret = binascii.hexlify(os.urandom(24))

def create_app(config_name):
    # from app.v1.views.decorators import login_required
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = secret
    app.config["SWAGGER"] = {
        "title": "BOOK-A-MEAL",
        "version": 1,
    }
    # with app.app_context():
    #     db.init_app(app)
    #     db.create_all()

    return app

app1 = create_app("development")
