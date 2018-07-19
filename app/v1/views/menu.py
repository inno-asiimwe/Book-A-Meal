from flask import jsonify, request, Blueprint
from flasgger import swag_from
from app.v1.views.decorators import login_required
from marshmallow import ValidationError
from app.v1.models.models import Menu, menu_schema


menu = Blueprint('menu', __name__, url_prefix='/api/v1')


@menu.route("/menu")
@swag_from('api_doc/get_menu.yml')
@login_required
def get_menu():
    """Get menu available"""
    return Menu.get_menu()


@menu.route("/menu", methods=["POST"])
@swag_from('api_doc/setup_menu.yml')
@login_required
def setup_menu():
    """Enables menu setup"""
    data = request.data
    try:
        menu_data = menu_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages)
    id = menu_data["meal_id"]
    return Menu.setup_menu(id)
