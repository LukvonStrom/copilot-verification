from flask import Flask
from src.flask.config import Config
from src.database.database import init_db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from src.flask.routes import main_bp

    app.register_blueprint(main_bp)

    with app.app_context():
        init_db()

    return app
