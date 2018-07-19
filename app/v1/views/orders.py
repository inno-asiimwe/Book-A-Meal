from flask import jsonify, request, make_response, Blueprint
from flasgger import swag_from
from app.v1.views.decorators import login_required
from app.v1.models.models import Order, order_schema
from marshmallow import ValidationError


orders = Blueprint('orders', __name__, url_prefix='/api/v1')


@orders.route("/orders")
@login_required
@swag_from('api_doc/get_all_orders.yml')
def get_all_orders():
    orders = Order.get_all_orders()
    if orders:
        results = []
        for order in orders:
            obj = {
                "id": order.id,
                "order_time": order.order_time
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response
    else:
        return make_response("No orders present", 400)


@orders.route("/orders/<int:id>", methods=["DELETE"])
@login_required
@swag_from('api_doc/delete_order.yml')
def remove_order(id):
    order = Order.query.filter_by(id=id).first()
    if not order:
        return make_response(
            "The order specified is not present"), 400
    Order.session.delete(order)
    response = make_response(
        "The order has been deleted", 200)
    return response


@orders.route("/orders/", methods=["POST"])
@login_required
@swag_from('api_doc/setup_order.yml')
def account_create_order():
    """Enables order setup"""
    data = request.data
    try:
        order_data = order_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages)
    id = order_data["menu_id"]
    return Order.setup_order(id)
