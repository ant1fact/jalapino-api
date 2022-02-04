from flask import Flask
from flask_migrate import Migrate
from . import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    from .models import db

    db.init_app(app)
    Migrate(app, db)

    from .api import api
    app.register_blueprint(api)

    @app.route('/')
    def index():
        return 'JalAPIño 🌶️'

    return app