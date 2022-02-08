import json

from flask import Blueprint, abort, jsonify, request
from werkzeug.exceptions import HTTPException

from .auth import AuthError, requires_auth

api = Blueprint('api', __name__)

from .config import Config
from .models import Category, Customer, Ingredient, Item, Restaurant

### RESTAURANTS ###


@requires_auth('create:restaurant')
@api.route('/restaurants', methods=['POST'])
def create_restaurant(payload):
    '''Create a restaurant resource once per auth0 restaurant registration.'''
    # If requester's auth0 id already exists, return the associated resource instead
    if Restaurant.query.filter_by(auth0_id=payload['sub']).first() is not None:
        return get_restaurant_by_id(), 302
    # Get request body and attach auth0 id from payload
    body = request.get_json()
    body['auth0_id'] = payload['sub']
    # Make sure request body contains data for non-nullable columns in the DB
    for field in Restaurant.required_fields():
        field_data = body.get(field, None)
        if field_data in {'', None}:
            abort(400)
    # Create empty resource, add data from request body and save to DB
    new_restaurant = Restaurant()
    new_restaurant.update(body)
    new_restaurant.save()

    return {'id': new_restaurant.id}, 201


@api.route('/restaurants')
def get_restaurants():
    '''Return a list of all restaurants with active status paginated. For a list of all
    deactivated restaurants the request body must contain {'is_active': False}'''
    page = request.args.get('page', 1, type=int)
    # Check if the request body specifies active vs inactive records
    body = request.get_json()
    is_active = body.get('is_active', True)
    restaurants = Restaurant.query.filter_by(is_active=is_active).paginate(
        page=page, per_page=Config.RESULTS_PER_PAGE
    )
    return jsonify([r.serialize() for r in restaurants])


@api.route('/restaurants/<int:id>')
def get_restaurant_by_id(id: int):
    return Restaurant.query.get_or_404(id).serialize()


@requires_auth('update:restaurant')
@api.route('/restaurants/<int:id>', methods=['PATCH'])
def update_restaurant(payload: dict, id: int):
    restaurant = Restaurant.get_or_404(id)
    # Check that requester is the owner of the resource
    if restaurant.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    restaurant.update(body)
    restaurant.save()
    return get_restaurant_by_id(id)


@requires_auth('admin')
@api.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id: int):
    restaurant = Restaurant.query.get_or_404(id)
    restaurant.delete()


### CUSTOMERS ###

@requires_auth('create:customer')
@api.route('/customers', methods=['POST'])
def create_customer(payload):
    '''Create a customer resource once per auth0 customer registration.'''
    # If requester's auth0 id already exists, return the associated resource instead
    if Customer.query.filter_by(auth0_id=payload['sub']).first() is not None:
        return get_customer_by_id(), 302
    # Get request body and attach auth0 id from payload
    body = request.get_json()
    body['auth0_id'] = payload['sub']
    # Make sure request body contains data for non-nullable columns in the DB
    for field in Customer.required_fields():
        field_data = body.get(field, None)
        if field_data in {'', None}:
            abort(400)
    # Create empty resource, add data from request body and save to DB
    new_customer = Customer()
    new_customer.update(body)
    new_customer.save()

    return {'id': new_customer.id}, 201


@requires_auth('admin')
@api.route('/customers')
def get_customers():
    '''Return a list of all customers with active status paginated. For a list of all
    deactivated customers the request body must contain  {'is_active': False}
    NOTE: For data protection, this endpoint is only available to admins.'''
    page = request.args.get('page', 1, type=int)
    # Check if the request body specifies active vs inactive records
    body = request.get_json()
    is_active = body.get('is_active', True)
    customers = Customer.query.filter_by(is_active=is_active).paginate(
        page=page, per_page=Config.RESULTS_PER_PAGE
    )
    return jsonify([c.serialize() for c in customers])


@requires_auth('read:customer')
@api.route('/customers/<int:id>')
def get_customer_by_id(payload: dict, id: int):
    customer = Customer.query.get_or_404(id)
    if customer.auth0_id != payload['sub']:
        abort(403)
    return Customer.query.get_or_404(id).serialize()


@requires_auth('update:customer')
@api.route('/customers/<int:id>', methods=['PATCH'])
def update_customer(payload: dict, id: int):
    customer = Customer.get_or_404(id)
    # Check that requester is the owner of the resource
    if customer.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    customer.update(body)
    customer.save()
    return get_restaurant_by_id(id)


@requires_auth('admin')
@api.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id: int):
    customer = Customer.query.get_or_404(id)
    customer.delete()


### CATEGORIES ###

@api.route('/categories')
def get_categories():
    '''Return a list of all categories paginated.'''
    page = request.args.get('page', 1, type=int)
    categories = Category.query.paginate(page=page, per_page=Config.RESULTS_PER_PAGE)
    return jsonify([c.serialize() for c in categories])


@api.route('/restaurants/<int:id>/categories')
def get_restaurant_categories(id: int):
    '''Get all categories specific to a restaurant.'''
    return jsonify([c.serialize() for c in Restaurant.query.get_or_404(id).categories])


@requires_auth('create:category')
@api.route('/restaurants/<int:id>/categories', methods=['POST'])
def get_restaurant_categories(payload: dict, id: int):
    restaurant = Restaurant.get_or_404(id)
    if restaurant.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    # Require minimum information for creating a new category
    if body.get('restaurant_id', 0) != restaurant.id or not body.get('name', ''):
        abort(400)
    new_category = Category()
    new_category.update(body)
    new_category.save()
    return {'id': new_category.id}, 201


### ITEMS AND INGREDIENTS ###


@api.route('/items')
def get_items():
    '''Return a list of all items paginated.'''
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(page=page, per_page=Config.RESULTS_PER_PAGE)
    return jsonify([i.serialize() for i in items])


def get_or_create_ingredient(ingredient_name: str) -> Ingredient:
    '''Helper function for create_item endpoint.'''
    ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
    if ingredient is not None:
        return ingredient
    new_ingredient = Ingredient(name=ingredient_name)
    new_ingredient.save()
    return new_ingredient


@requires_auth('create:item')
@api.route('/categories/<int:id>/items', methods=['POST'])
def create_item(payload: dict, id: int):
    category = Category.query.get_or_404(id)
    restaurant = Restaurant.query.get_or_404(category.restaurant_id)
    # Check that requester is the owner of the resource
    if restaurant.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    for field in Item.required_fields():
        if field not in body:
            abort(400)
    new_item = Item()
    # First take care of converting any ingredient names to ingredient objects
    if body.get('ingredients', []):
        # Remove original ingredients list from message body using .pop()
        # so it doesn't revert when calling .update() on the new item
        new_item.ingredients = [
            get_or_create_ingredient(ingredient_name)
            for ingredient_name in body.pop('ingredients')
        ]
    # Add remaining data to transient Item record
    new_item.update(body)
    new_item.save()
    return {'id': new_item.id}, 201


@requires_auth('admin')
@api.route('/ingredients/<int:id>', methods=['DELETE'])
def delete_ingredient(id: int):
    ingredient = Ingredient.query.get_or_404(id)
    ingredient.delete()
    return {'id': id}


### ORDERS ###


### ERROR HANDLING ###

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
