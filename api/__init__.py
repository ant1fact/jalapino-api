from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from . import config


def create_app(config=config.Config):
    app = Flask(__name__)
    app.config.from_object(config)

    from .models import db

    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    from .api import api

    app.register_blueprint(api)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization'
        )
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE'
        )
        return response

    return app
