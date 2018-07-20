from flask import request, make_response, Blueprint, jsonify
from flasgger import swag_from
from app.v1.views.decorators import login_required
from app.v1.models.models import Order



orders = Blueprint('orders', __name__, url_prefix='/api/v1')


@orders.route("/orders")
@swag_from('api_doc/get_all_orders.yml')
# @login_required
def get_all_orders():
    orders = Order.get_all_orders()
    if orders:
        return jsonify({"orders": orders}), 200
    return make_response("No orders present", 400)


@orders.route("/orders/<int:id>", methods=["DELETE"])
@swag_from('api_doc/delete_order.yml')
# @login_required
def remove_order(id):
    if Order.delete_order(id):
        return jsonify({"message": "The order has been deleted"}), 200
    return jsonify({"message": "The order specified is not present"}), 400


@orders.route("/orders", methods=["POST"])
@swag_from('api_doc/setup_order.yml')
# @login_required
def account_create_order():
    """Enables order setup"""
    data = request.data
    id = data["menu_id"]
    if Order(menu_id=id).setup_order():
        return jsonify({'message':'Your Order has been Created'}), 201
    return jsonify({"message":'Menu Id Inexistent'}), 200
