import os
import unittest

from app.v1.views.meals import meals
from app.v1.views.menu import menu
from app.v1.views.users import users
from app.v1.views.orders import orders

from run_setup import app, app1, create_app


from flasgger import Swagger

swagger = Swagger(app)


def start_app():
    app1.register_blueprint(users)
    app1.register_blueprint(meals)
    app1.register_blueprint(menu)
    app1.register_blueprint(orders)
    return app1


if __name__ == '__main__':
    start_app().run()

