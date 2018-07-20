from flask import jsonify, request, Blueprint
from flasgger import swag_from
from marshmallow import ValidationError
from app.v1.models.models import User, user_schema
from app.v1.views.authentication import Token


users = Blueprint('users', __name__, url_prefix='/auth')


@users.route("/register", methods=["POST"])
@swag_from('apidocs/user_signup.yml')
def register_user():
    post_data = request.data
    try:
        user_data = user_schema.load(post_data)
    except ValidationError as e:
        return jsonify(e.messages), 401
    else:
        email, password = user_data["email"], user_data["password"]
        user = User.create_user(email, password)
        if user:
            return jsonify({
                "id": user.id,
                "email": user.email
            }), 201
        return jsonify({"message": "User already exists. Please login."}), 403


@users.route("/login", methods=["POST"])
@swag_from('apidocs/user_login.yml')
def login_user():
    """Handle POST request for this view. Url --> /auth/login"""
    login_data = request.data
    email, password = login_data["email"], login_data["password"]
    user = User.login_user(email, password)
    if user:

        token = Token()
        access_token = token.generate_token(user.id)
        if access_token:
            return jsonify({
                "message": "You logged in successfully.",
                "access_token": access_token.decode()
            }), 200
        return jsonify({"message": "Invalid email or password, Please try again"}), 401
    return jsonify({"message": "Please register then login"}), 500

