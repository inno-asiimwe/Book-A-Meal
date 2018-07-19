from flask import jsonify, request, Blueprint
from flasgger import swag_from
from app.v1.views.decorators import login_required
from marshmallow import ValidationError
from app.v1.models.models import Meal, meal_schema

meals = Blueprint('meals', __name__, url_prefix='/api/v1')


@meals.route("/meals")
@login_required
@swag_from('api_doc/get_meals.yml')
def account_get_meals():
    return Meal.get_meals()


@meals.route("/meals/<int:id>", methods=["GET"])
@login_required
@swag_from('api_doc/get_meal.yml')
def account_get_specific_meal(id):
    return Meal.get_meal(id)


@meals.route("/meals", methods=["POST"])
@login_required
@swag_from('api_doc/create_meal.yml')
def account_create_meal():
    data = request.data
    try:
        meal_data = meal_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages)

    name, price = meal_data["name"], meal_data["price"]
    return Meal.create_meal(name, price)


@meals.route("/meals/<int:id>", methods=["PUT"])
@login_required
@swag_from('api_doc/update_meal.yml')
def account_update_meal(id):
    name = request.data["name"]
    price = request.data["price"]
    return Meal.update_meal(id, name, price)


@meals.route("/meals/<int:id>", methods=["DELETE"])
@login_required
@swag_from('api_doc/delete_meal.yml')
def account_delete_meal(id):
    return Meal.delete_meal(id)
