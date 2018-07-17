db = SQLAlchemy()
secret = binascii.hexlify(os.urandom(24))

app = FlaskAPI(__name__, instance_relative_config=True)

def create_app(config_name):

    from .decorators import login_required

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = secret
    with app.app_context():
        db.init_app(app)
        db.create_all()

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app