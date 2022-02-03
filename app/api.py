from flask import Blueprint, jsonify
from .auth import AuthError

api = Blueprint('api', __name__)

from .models import Restaurant


@api.route('/restaurants')
def get_restaurants():
    return jsonify(
        [
            {
                'id': r.id,
                'name': r.name,
                'logo_uri': r.logo_uri,
                'description': r.description,
            }
            for r in Restaurant.query.all()
        ]
    )


# https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.errorhandler
@api.errorhandler(AuthError)
def handle_auth_error(e):
    return e.error, e.status_code
