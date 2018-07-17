from flask import Blueprint

orders = Blueprint('orders', __name__, url_prefix='/api/v1')

@orders.route("/orders")
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
def remove_order(id):
    order = Order.query.filter_by(id=id).first()
    if not order:
        return make_response(
            "The order specified is not present"), 400
    Order.session.delete(order)
    response = make_response(
        "The order has been deleted", 200)
    return response
