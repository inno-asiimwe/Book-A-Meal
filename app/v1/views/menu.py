from flask import jsonify, make_response, request, Blueprint
from flasgger import swag_from
from app.v1.views.decorators import login_required
from marshmallow import ValidationError
from app.v1.models.models import Menu, menu_schema
from datetime import datetime


menu = Blueprint('menu', __name__, url_prefix='/api/v1')


@menu.route("/menu")
@swag_from('apidocs/get_menu.yml')
@login_required
def get_menu():
    """Get menu available"""
    response = Menu.get_menu()
    if response:
        return jsonify({"Menu": response}), 200
    return make_response("No menu present", 400)


@menu.route("/menu", methods=["POST"])
@swag_from('apidocs/setup_menu.yml')
@login_required
def setup_menu():
    """Enables menu setup"""
    data = request.data
    try:
        menu_data = menu_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages)
    id = menu_data["meal_id"]
    menu = Menu.setup_menu(id)
    if menu:
        return jsonify({
            'id': menu.id,
            'name': menu.meal.name,
            'price': menu.meal.price,
            'day': datetime.utcnow()
        }), 201
    return "Invalid Meal id", 400 
