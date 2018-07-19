from datetime import datetime
from flask import jsonify, make_response
from app.v1.models.db_connect import db


class Order(db.Model):
    """Defines the 'Order' mapped to database table 'order'."""
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    order_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user_id, menu_id):
        """Initialises the order tables"""
        self.user_id = user_id
        self.menu_id = menu_id

    # @staticmethod
    # def setup_menu(id):
    #     """Creates the menu"""
    #     menu = Menu(meal_id=id)
    #     menu.save()
    #     return make_response(
    #         {"MENU": {
    #             'id': menu.id,
    #             'name': menu.meal.name,
    #             'price': menu.meal.price,
    #             'day': datetime.utcnow()
    #         }
    #         }), 201

    def setup_order(id):
        """Creates the order"""
        order = Order(order_id=id)
        Order.save()
        return make_response(
            {"ORDER":{
                "id": order.id,
                "name":Order.menu_id
            }}
        )

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
        orders = []
        raw_orders = Order.query.all()
        for order in raw_orders:
            orders.append(order.to_dictionary())
        return orders

    def to_dictionary(self):
        """Return a dictionary representation of the order"""
        return dict(
            order_id=self.id,
            user_id=self.user_id,
            meal=self.menu.meal.name,
            price=self.menu.meal.price,
            order_time=self.order_time)

    def __repr__(self):
        """Returns a string representation of the order table"""
        return "Order(%d, %s, %s, %s, %s )" % (
            self.id, self.menu_name, self.admin_id, self.order_time, self.user_id)


class OrderSchema(Schema):
    """Defines a Order Schema"""
    id = fields.Int(dump_only=True)
    menu_id = fields.Int(required=True, validate=must_not_be_black)
    day = fields.Date(dump_only=True)


order_schema = MenuSchema()
