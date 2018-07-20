from flask_bcrypt import Bcrypt
from flask import request
from app.v1.models.db_connect import db
from marshmallow import Schema, fields, validate, ValidationError


class User(db.Model):
    """Defines the 'User' model mapped to database table 'user'."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(145), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    admin = db.Column(db.Boolean, default=False)


    def __init__(self, email, password):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

    def password_is_valid(self, password):
        """Checks the password against its hash to validate the user's password"""
        return Bcrypt().check_password_hash(self.password, password)

    def __repr__(self):
        """Returns a User model representation"""
        return "User (%d, %s, %s, %s)" % (
            self.id, self.email, self.admin, self.orders)

    def save(self):
        """Save a user to the database."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def create_user(email, password):
        user = User.query.filter_by(email=request.data["email"]).first()
        if not user:
            user = User(email, password)
            user.save()
            created_user = User.query.filter_by(email=request.data["email"]).first() 
            return created_user
        else:
            return False

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=request.data["email"]).first()
        if user and user.password_is_valid(request.data["password"]):
            return user
        return False


def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided")


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True,
                         validate=(validate.Length(min=8, max=100)))
    password = fields.Str(required=True, 
                          validate=(must_not_be_blank,
                                    validate.Length(min=8, max=100)))


user_schema = UserSchema()
