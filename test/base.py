import flask_testing
from app import blueprint
from app.main import create_app


class BaseTestCase(flask_testing.TestCase):
    def create_app(self):
        app = create_app('test')
        app.register_blueprint(blueprint)
        app.app_context().push()
        return app
