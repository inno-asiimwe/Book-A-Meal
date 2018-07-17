from flask import Blueprint

meals = Blueprint('meals', __name__, url_prefix='/api/v1')

@meals.route("/meals")
@login_required
def account_get_meals():
    return Meal.get_meals()

@meals.route("/meals/<int:id>", methods=["GET"])
@login_required
def account_get_specific_meal(id):
    return Meal.get_meal(id)

@meals.route("/meals", methods=["POST"])
@login_required
def account_create_meal():
    data = request.data
    name = data["name"]
    price = data["price"]
    return Meal.create_meal(name, price)

@meals.route("/meals/<int:id>", methods=["PUT"])
def account_update_meal(id):
    name = request.data["name"]
    price = request.data["price"]
    return Meal.update_meal(id, name, price)

@meals.route("/meals/<int:id>", methods=["DELETE"])
def account_delete_meal(id):
    return Meal.delete_meal(id)
