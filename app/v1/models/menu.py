from datetime import datetime, timedelta
from flask import jsonify, make_response
from app.v1.models.db_connect import db
from marshmallow import Schema, fields, validate, ValidationError


class Menu(db.Model):
    """Defines the 'Menu' model mapped to table 'menu'."""
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    day = db.Column(db.DateTime, default=datetime.today())
    orders = db.relationship('Order', backref='menu')


    def __init__(self, meal_id):
        """Initialises the menu model"""
        self.meal_id = meal_id

    def save(self):
        """Saves items to the menu table"""
        self.day = datetime.today()
        db.session.add(self)
        try:
            db.session.commit()
        except BaseException:
            db.session.rollback()

    @staticmethod
    def get_menu():
        """Retrieves all the menu items"""
        menus = Menu.query.all()
        print(menus)
        if not menus:
            return make_response("No menu present", 400)
        
        results = []
        for menu in menus:
            # obj = menu_schema.dump(menu)
            obj = {
                'id': menu.id,
                'name': menu.meal.name,
                'price': menu.meal.price,
                'day': menu.day
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @staticmethod
    def setup_menu(id):
        """Creates the menu"""
        menu = Menu(meal_id=id)
        menu.save()
        return make_response(
            {"MENU": {
                'id': menu.id,
                'name': menu.meal.name,
                'price': menu.meal.price,
                'day': datetime.utcnow()
            }
            }), 201

    def __repr__(self):
        """Returns a string representation of menu object"""
        return "Menu (%d,%s, %s, %s, %s )" % (
            self.id, self.meal.name, self.meal.price, self.meal_id, self.day)


def must_not_be_black(data):
    """Ensures data retrieved is not blank"""
    if not data:
        raise ValidationError("Data not provided")


class MenuSchema(Schema):
    """Defines a Menu Schema"""
    id = fields.Int(dump_only=True)
    meal_id = fields.Int(required=True, validate=must_not_be_black)
    day = fields.Date(dump_only=True)


menu_schema = MenuSchema()
menus_schema = MenuSchema(many=True)  
