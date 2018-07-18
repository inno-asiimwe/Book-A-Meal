from flask import jsonify, request, make_response, Blueprint
from flasgger import swag_from
import re
from app.v1.models.models import User
import os
import binascii
from app.v1.views.authentication import Token


users = Blueprint('users', __name__, url_prefix='/auth')


@users.route("/register", methods=["POST"])
def register_user():
    user = User.query.filter_by(email=request.data["email"]).first()
    if not user:
        try:
            message = "Wrong email or password"
            status_code = 400
            post_data = request.data
            email = post_data["email"]
            password = post_data["password"]
            if email and password:
                if not re.match(
                        r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
                    return message, status_code

                if password.strip() == "":
                    return message, status_code

                if not re.match("\d.*[A-Z]|[A-Z].*\d", password):
                    raise AssertionError(
                        "Password must contain 1 capital letter and 1 number")

                if len(password) < 8 or len(password) > 50:
                    raise AssertionError(
                        "Password must be between 8 and 50 characters")

                user = User(email=email, password=password)
                user.save()
                response = {
                    "message": "You registered successfully."
                }
                return make_response(jsonify(response)), 201
            return message, 404

        except Exception as e:
            response = {
                "message": str(e)
            }
            return make_response(jsonify(response)), 401
    else:
        response = {
            "message": "User already exists. Please login."
        }
        return make_response(jsonify(response)), 202


@users.route("/login", methods=["POST"])
def login_user():
    """Handle POST request for this view. Url --> /auth/login"""
    try:
        user = User.query.filter_by(email=request.data["email"]).first()

        if user and user.password_is_valid(request.data["password"]):
            token = Token()
            access_token = token.generate_token(user.id)
            if access_token:
                response = {
                    "message": "You logged in successfully.",
                    "access_token": access_token.decode()
                }
                return make_response(jsonify(response)), 200
        else:
            response = {
                "message": "Invalid email or password, Please try again"
            }
            return make_response(jsonify(response)), 401

    except Exception as e:
        response = {
            "message": str(e)
        }
        return make_response(jsonify(response)), 500
