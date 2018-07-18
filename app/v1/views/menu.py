from flask import jsonify, request, make_response, Blueprint
from flasgger import swag_from
from app.v1.views.decorators import login_required
from app.v1.models.models import Menu


menu = Blueprint('menu', __name__, url_prefix='/api/v1')

@menu.route("/menu")
@swag_from('api_doc/get_menu.yml')
def get_menu():
    return Menu.get_menu()

@menu.route("/menu", methods=["POST"])
@swag_from('api_doc/setup_menu.yml')
def setup_menu():
    data = request.data
    id = data['meal_id']
    if id:
        return Menu.setup_menu(id)
