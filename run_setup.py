from flask_api import FlaskAPI
import os
import binascii

from instance.config import app_config

app = FlaskAPI(__name__, instance_relative_config=True)

secret = binascii.hexlify(os.urandom(24))


def create_app(config_name):
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = secret
    app.config["SWAGGER"] = {
        "title": "BOOK-A-MEAL",
        "version": 1,
    }

    return app


app1 = create_app("development")
