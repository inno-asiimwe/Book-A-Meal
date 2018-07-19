import unittest
from run_setup import app1
from app.v1.models.db_connect import db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app1, db)
manager = Manager(app1)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
