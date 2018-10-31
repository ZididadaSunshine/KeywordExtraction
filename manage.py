from flask_script import Manager
from app import blueprint
from app.main import create_app

app = create_app()
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
