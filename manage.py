import os
import unittest

from app.v1.views.meals import meals
from app.v1.views.menu import menu
from app.v1.views.users import users
from app.v1.views.orders import orders

from run_setup import app, app1, create_app


from flasgger import Swagger

# app = create_app(config_name=os.getenv('APP_SETTINGS'))

# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand

# migrate = Migrate(app, db)
# manager = Manager(app)

# manager.add_command('db', MigrateCommand)

# @manager.command
# def test():
#     """Runs the unit tests without test coverage."""
#     tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.wasSuccessful():
#         return 0
#     return 1

swagger = Swagger(app)

app1.register_blueprint(users)
app1.register_blueprint(meals)
app1.register_blueprint(menu)
app1.register_blueprint(orders)


if __name__ == '__main__':
    app1.run()
    # manager.run()
