from flask import Flask

from .config import config_by_name


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_by_name['dev'])

    return app
