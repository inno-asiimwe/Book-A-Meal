import os

from app.v1.views.api import create_app

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == "__main__":
    app.run()
