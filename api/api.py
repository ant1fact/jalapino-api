import json

from flask import Blueprint, abort, jsonify, request
from werkzeug.exceptions import HTTPException

from .auth import AuthError, requires_auth

api = Blueprint('api', __name__)

from .config import Config
from .models import Restaurant


@api.route('/restaurants')
def get_restaurants():
    '''Return a list of all restaurants paginated.'''
    page = request.args.get('page', 1, type=int)
    # Number of results per page can be changed in config.py
    restaurants = Restaurant.query.paginate(
        page=page, per_page=Config.RESTAURANTS_PER_PAGE
    )
    return jsonify([r.serialize() for r in restaurants])


@api.route('/restaurants/<int:id>')
def get_restaurant(id: int):
    return Restaurant.query.get_or_404(id).serialize()


@api.route('/restaurants/<int:id>/categories')
def get_restaurant_categories(id: int):
    return jsonify([c.serialize() for c in Restaurant.query.get_or_404(id).categories])


@requires_auth('create:restaurant')
@api.route('/restaurants', methods=['POST'])
def create_restaurant(payload):
    body = request.get_json()
    # Store requester's auth0_id with the restaurant's record
    body['auth0_id'] = payload['sub']
    # Make sure request body contains data for non-nullable columns in the DB
    for field in Restaurant.required_fields():
        field_data = body.get(field, None)
        if field_data in {'', None}:
            abort(400)
    # Create empty record, add data from request body and save to DB
    new_restaurant = Restaurant()
    new_restaurant.update(body)
    new_restaurant.save()

    return {'id': new_restaurant.id}, 201


@requires_auth('update:restaurant')
@api.route('/restaurants/<int:id>', methods=['PUT', 'PATCH'])
def update_restaurant(payload, id: int):
    restaurant = Restaurant.get_or_404(id)
    if restaurant.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    if request.method == 'PATCH':
        restaurant.update(body)
        restaurant.save()
        return get_restaurant(id)
    for key in restaurant.serialize():
        if key not in body:
            abort(400)
    restaurant.update(body)
    restaurant.save()
    return get_restaurant(id)


# https://flask.palletsprojects.com/en/2.0.x/errorhandling/#generic-exception-handlers
@api.errorhandler(HTTPException)
def handle_exception(e):
    '''Return JSON instead of HTML for HTTP errors.'''
    # Start with the correct headers and status code from the error
    response = e.get_response()
    # Replace the body with JSON
    response.data = json.dumps(
        {'code': e.code, 'name': e.name, 'description': e.description}
    )
    response.content_type = 'application/json'
    return response


# https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.errorhandler
@api.errorhandler(AuthError)
def handle_auth_error(e):
    return e.error, e.status_code
