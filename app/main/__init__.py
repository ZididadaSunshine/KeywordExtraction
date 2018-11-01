from flask import Flask

from .config import config_by_name


def create_app(config='prod'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config])

    return app
