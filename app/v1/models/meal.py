from flask import jsonify, make_response
from app.v1.models.db_connect import db

from marshmallow import Schema, fields, validate, ValidationError


class Meal(db.Model):
    """Defines the 'Meal' model mapped to database table 'meal'."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(46), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    menus = db.relationship('Menu', backref='meal')

    def __init__(self, name, price):
        """Initialises the meal model"""
        self.name = name
        self.price = price

    def save(self):
        """Saves item to the Meal table"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Removes item from meal table"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_meals():
        """Retrieves all meals present in the meal table"""
        results = []
        meals = Meal.query.all()
        if meals:
            for meal in meals:
                obj = meal_schema.dump(meal)
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
        else:
            return "No meals present", 400

    @staticmethod
    def get_meal(id):
        """Helps to get a specific meal"""
        meal = Meal.query.filter_by(id=id).first()
        if not meal:
            return make_response("That meal is not present", 400)
        results = []
        obj = meal_schema.dump(meal)
        results.append(obj)
        return make_response(jsonify(results), 200)

    @staticmethod
    def create_meal(name, price):
        """Enables meal creation"""
        meal = Meal.query.filter_by(name=name).first()
        if not meal:
            meal = Meal(name, price)
            meal.save()
            result = meal_schema.dump(meal)
            response = jsonify(result),201
            return response
        else:
            return make_response("The meal already exists", 400)

    @staticmethod
    def update_meal(id, name, price):
        """Enables meal change"""
        meal = Meal.query.filter_by(id=id).first()
        if not meal:
            abort(404)

        meal.name = name
        meal.price = price
        meal.save()
        result = meal_schema.dump(meal)
        response = jsonify(result), 200
        return response

    @staticmethod
    def delete_meal(id):
        """Helps one remove a specific meal"""
        meal = Meal.query.filter_by(id=id).first()
        if meal:
            Meal.delete(meal)
            response = make_response(
                'The meal has been deleted', 200)
            return response
        return "The meal specified is not present", 400

    def __repr__(self):
        """Returns a representation of the meals"""
        return "Meal (%d, %s, %s )" % (
            self.id, self.name, self.price)


def must_not_be_black(data):
    """Ensures no empty data is retrieved"""
    if not data:
        raise ValidationError("Data not provided")


class MealSchema(Schema):
    """Defines the Meal Schema"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True,
                      validate=(must_not_be_black, 
                                validate.Length(min=2, max=46)))
    price = fields.Int(required=True)


meal_schema = MealSchema()
meals_schema = MealSchema(many=True)
