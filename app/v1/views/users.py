from flask import jsonify, request, make_response, Blueprint
from flasgger import swag_from
from app.v1.views.authentication import Token
from marshmallow import ValidationError
from app.v1.models.user import User, user_schema


users = Blueprint('users', __name__, url_prefix='/auth')

@users.route("/register", methods=["POST"])
def register_user():
    post_data = request.data
    try:
        user_data = user_schema.load(post_data)
    except ValidationError as e:
        return jsonify(e.messages), 401
    else:
        email, password = user_data["email"], user_data["password"]
        return User.create_user(email, password)


@users.route("/login", methods=["POST"])
def login_user():
    """Handle POST request for this view. Url --> /auth/login"""
    login_data = request.data
    email, password = login_data["email"], login_data["password"]
    return User.login_user(email, password)
