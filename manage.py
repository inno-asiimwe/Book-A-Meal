from app.v1.views.meals import meals
from app.v1.views.menu import menu
from app.v1.views.users import users
from app.v1.views.orders import orders

from run_setup import app, app1


from flasgger import Swagger




def start_app():
    
    app1.register_blueprint(users)
    app1.register_blueprint(meals)
    app1.register_blueprint(menu)
    app1.register_blueprint(orders)
    swagger = Swagger(app1)
    return app1

app = start_app()


if __name__ == '__main__':
    app.run()
