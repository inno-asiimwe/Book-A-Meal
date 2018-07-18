from app.v1.models.db_connect import db
from app.v1.models.user import User
from app.v1.models.meal import Meal
from app.v1.models.menu import Menu
from app.v1.models.order import Order

db.create_all()
