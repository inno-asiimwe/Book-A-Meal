from flask import jsonify, request, make_response, Blueprint
from flasgger import swag_from
from app.v1.views.decorators import login_required
from app.v1.models.models import Order, order_schema
from marshmallow import ValidationError


orders = Blueprint('orders', __name__, url_prefix='/api/v1')


@orders.route("/orders")
@swag_from('api_doc/get_all_orders.yml')
@login_required
def get_all_orders():
    return Order.get_all_orders()


@orders.route("/orders/<int:id>", methods=["DELETE"])
@swag_from('api_doc/delete_order.yml')
@login_required
def remove_order(id):
    return Order.delete_order(id)


@orders.route("/orders", methods=["POST"])
@swag_from('api_doc/setup_order.yml')
@login_required
def account_create_order():
    """Enables order setup"""
    data = request.data
    id = data["menu_id"]
    return Order(menu_id=id).setup_order()
