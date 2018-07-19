from app.v1.models.db_connect import db
from app.v1.models.user import User, user_schema
from app.v1.models.meal import Meal, meal_schema
from app.v1.models.menu import Menu, menu_schema
from app.v1.models.order import Order, order_schema

db.create_all()
