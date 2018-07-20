from flask import jsonify, make_response, request, Blueprint
from flasgger import swag_from
from app.v1.views.decorators import login_required
from marshmallow import ValidationError
from app.v1.models.models import Meal, meal_schema

meals = Blueprint('meals', __name__, url_prefix='/api/v1')


@meals.route("/meals")
@swag_from('api_doc/get_meals.yml')
# @login_required
def account_get_meals():
    meals = Meal.get_meals()
    if meals:
        return jsonify({"Meals": meals}), 200
    return "No meals present", 400


@meals.route("/meals/<int:id>", methods=["GET"])
@swag_from('api_doc/get_meal.yml')
# @login_required
def account_get_specific_meal(id):
    meal = Meal.get_meal(id)
    if meal:
        return jsonify({"Meal": meal}), 200
    return make_response("That meal is not present", 400)


@meals.route("/meals", methods=["POST"])
# @login_required
@swag_from('api_doc/create_meal.yml')
def account_create_meal():
    data = request.data
    try:
        meal_data = meal_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages)

    name, price = meal_data["name"], meal_data["price"]
    meal = Meal.create_meal(name, price)
    if meal:
        return jsonify(meal), 201
    else:
        return make_response("The meal already exists", 400)


@meals.route("/meals/<int:id>", methods=["PUT"])
# @login_required
@swag_from('api_doc/update_meal.yml')
def account_update_meal(id):
    name = request.data["name"]
    price = request.data["price"]
    meal = Meal.update_meal(id, name, price)
    if meal:
        return jsonify(meal), 200
    else:
        return jsonify({"message":"The meal specified is not present"}), 400


@meals.route("/meals/<int:id>", methods=["DELETE"])
# @login_required
@swag_from('api_doc/delete_meal.yml')
def account_delete_meal(id):
    meal = Meal.delete_meal(id)
    if not meal:
        return "The meal specified is not present", 400
    else:
        return make_response(
                 'The meal has been deleted', 200)
