from datetime import datetime
from flask import jsonify, make_response
from app.v1.models.db_connect import db
from marshmallow import Schema, fields, ValidationError


class Order(db.Model):
    """Defines the 'Order' mapped to database table 'order'."""
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    order_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, menu_id):
        """Initialises the order tables"""
        self.menu_id = menu_id

    def setup_order(self):
        """Creates the order"""
        db.session.add(self)
        if self.save():
            return make_response(
                jsonify({'message':'ORDER CREATED'}), 201
        )
        return make_response(jsonify(dict(message='ORDER NOT CREATED')), 200)

    def add_order(self):
        """Saves items to the order table"""
        self.order_time = datetime.now()
        db.session.add(self)
        return Order.save()

    def delete(self, x):
        """Removes items from the order table"""
        db.session.delete(x)
        Order.save()

    @staticmethod
    def save():
        try:
            db.session.commit()
            return True
        except BaseException:
            db.session.rollback()
            return False

    @staticmethod
    def get_all_orders():
        """Retrieves all orders present"""
        orders = Order.query.all()
        results = []
        if orders:
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

    @staticmethod
    def delete_order(id):
        order = Order.query.filter_by(id=id).first()
        if not order:
            return make_response(
                "The order specified is not present"), 400
        Order.session.delete(order)
        response = make_response(
            "The order has been deleted", 200)
        return response 

    def __repr__(self):
        """Returns a string representation of the order table"""
        return "Order(%d, %s, %s, %s, %s )" % (
            self.id, self.menu_name, self.admin_id, self.order_time, self.user_id)


def must_not_be_black(data):
    """Ensures data retrieved is not blank"""
    if not data:
        raise ValidationError("Data not provided")


class OrderSchema(Schema):
    """Defines a Order Schema"""
    id = fields.Int(dump_only=True)
    menu_id = fields.Int(required=True, validate=must_not_be_black)
    day = fields.Date(dump_only=True)


order_schema = OrderSchema()
