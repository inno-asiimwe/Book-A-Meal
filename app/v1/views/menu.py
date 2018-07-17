from flask import Blueprint

menu = Blueprint('menu', __name__, url_prefix='/api/v1')

@menu.route("/menu")
def get_menu():
    return Menu.get_menu()

@menu.route("/menu", methods=["POST"])
def setup_menu():
    data = request.data
    id = data['meal_id']
    if id:
        return Menu.setup_menu(id)