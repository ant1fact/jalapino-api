import json
from os import getenv

from flask import (Blueprint, Response, abort, jsonify, redirect, request,
                   url_for)
from werkzeug.exceptions import HTTPException

from .auth import AuthError, requires_auth

api = Blueprint('api', __name__)

from .config import Config
from .models import Category, Customer, Ingredient, Item, Order, Restaurant, db


def _verify_ownership(Model, id: int, auth0_id: str):
    '''Verify ownership of, and return the resource being requested.'''
    resource = Model.query.get_or_404(id)
    if 'auth0_id' not in Model.__dict__:
        # No ownership detected, return resource
        return resource
    if resource.auth0_id != auth0_id:
        abort(403)
    return resource


def _prepare_request_data(Model):
    '''Central logic for preparing data coming from POST, PUT and PATCH requests.'''
    if request.method not in {'POST', 'PUT', 'PATCH'}:
        abort(405)
    if request.method == 'POST':
        # Requires: All data
        # Server fills in missing data with defaults, except where column.nullable=False
        # in which case the data must come from the client.
        # Raise 400 (Bad Request) if any data in the final representation is None.
        data = {**Model.defaults(), **request.get_json()}
        if None in data.values():
            abort(400)
        return data
    if request.method == 'PUT':
        # Requires: All data
        # All data must be provided by the client.
        # Raise 400 (Bad Request) if any data in the final representation is None.
        data = request.get_json()
        for k in Model.defaults():
            if k not in data or not data[k]:
                abort(400)
        return data
    if request.method == 'PATCH':
        # Requires: Some data
        # Raise 400 (Bad Request) if the final representation contains no data.
        # i.e. none of the incoming key:value pairs were valid and got filtered out
        data = {k: v for k, v in request.get_json().items() if k in Model.defaults()}
        if not data:
            abort(400)
        return data


### INFO ###


@api.route('/info')
def info():
    return {
        'title': 'Jalapino - Final project for Udacity Fullstack Nanodegree',
        'version': 0.1,
        'description': 'Simplified food delivery platform where restaurants can post their items and customers can place orders.',
        'contact': {
            'name': 'David Pacsuta',
            'email': 'jalapino.test@gmail.com',
            'url': 'https://github.com/ant1fact/jalapino',
        },
        'license': {'name': 'MIT', 'url': 'https://spdx.org/licenses/MIT.html'},
    }


### AUTH REDIRECTS ###


@api.route('/login')
def redirect_login():
    AUTH0_DOMAIN = getenv('AUTH0_DOMAIN')
    return redirect(f'https://{AUTH0_DOMAIN}/authorize', code=302)


@api.route('/callback')
@api.route('/logout')
def redirect_other():
    return redirect(url_for('root'), code=302)


### RESTAURANTS ###


@api.route('/restaurants')
def get_restaurants():
    '''Return a list of all restaurants paginated.'''
    page = request.args.get('page', 1, type=int)
    restaurants = Restaurant.query.paginate(
        page=page, per_page=Config.PAGINATE_RESULTS_PER_PAGE
    ).items
    return jsonify([r.serialize() for r in restaurants])


@api.route('/restaurants/<int:id>')
def get_restaurant(id: int):
    return Restaurant.query.get_or_404(id).serialize()


@api.route('/restaurants', methods=['POST'])
@requires_auth('create:restaurant')
def create_restaurant(payload: dict):
    new_restaurant = Restaurant()
    data = _prepare_request_data(Restaurant)
    new_restaurant.update(data)
    new_restaurant.auth0_id = payload['sub']

    return {'id': new_restaurant.save()}, 201


@api.route('/restaurants/<int:id>', methods=['PUT', 'PATCH'])
@requires_auth('update:restaurant')
def update_restaurant(payload: dict, id: int):
    restaurant = _verify_ownership(Restaurant, id, auth0_id=payload['sub'])
    data = _prepare_request_data(Restaurant)
    restaurant.update(data)
    restaurant.save()

    return Response(status=200)


@api.route('/restaurants/<int:id>', methods=['DELETE'])
@requires_auth('delete:restaurant')
def delete_restaurant(payload: dict, id: int):
    restaurant = _verify_ownership(Restaurant, id, auth0_id=payload['sub'])
    restaurant.delete()
    return Response(status=200)


### CUSTOMERS ###


@api.route('/customers/<int:id>')
@requires_auth('read:customer')
def get_customer(payload: dict, id: int):
    customer = _verify_ownership(Customer, id, auth0_id=payload['sub'])
    return customer.serialize()


@api.route('/customers', methods=['POST'])
@requires_auth('create:customer')
def create_customer(payload: dict):
    new_customer = Customer()
    data = _prepare_request_data(Customer)
    new_customer.update(data)
    new_customer.auth0_id = payload['sub']

    return {'id': new_customer.save()}, 201


@api.route('/customers/<int:id>', methods=['PATCH'])
@requires_auth('update:customer')
def update_customer(payload: dict, id: int):
    customer = _verify_ownership(Customer, id, auth0_id=payload['sub'])
    data = _prepare_request_data(Customer)
    customer.update(data)
    customer.save()
    return Response(status=200)


@api.route('/customers/<int:id>', methods=['DELETE'])
@requires_auth('delete:customer')
def delete_customer(payload: dict, id: int):
    customer = _verify_ownership(Customer, id, auth0_id=payload['sub'])
    customer.delete()
    return Response(status=200)


### CATEGORIES ###


@api.route('/restaurants/<int:id>/categories', methods=['POST'])
@requires_auth('create:category')
def create_category(payload: dict, id: int):
    restaurant = _verify_ownership(Restaurant, id, auth0_id=payload['sub'])
    new_category = Category()
    data = _prepare_request_data(Restaurant)
    new_category.update(data)
    new_category.restaurant_id = restaurant.id

    return {'id': new_category.save()}, 201


@api.route('/categories/<int:id>', methods=['PUT', 'PATCH'])
@requires_auth('update:category')
def update_category(payload: dict, id: int):
    category = Category.query.get_or_404(id)
    _verify_ownership(Restaurant, id=category.restaurant_id, auth0_id=payload['sub'])
    data = _prepare_request_data(Category)
    category.update(data)
    category.save()
    return Response(status=200)


@api.route('/categories/<int:id>', methods=['DELETE'])
@requires_auth('delete:category')
def delete_category(payload: dict, id: int):
    category = Category.query.get_or_404(id)
    _verify_ownership(Restaurant, id=category.restaurant_id, auth0_id=payload['sub'])
    # Remove children before deletion
    category.items = []
    category.delete()
    return Response(status=200)


### ITEMS AND INGREDIENTS ###


def _get_or_create_ingredient(ingredient_name: str) -> Ingredient:
    ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
    if ingredient is not None:
        return ingredient
    new_ingredient = Ingredient(name=ingredient_name)
    new_ingredient.save()
    return new_ingredient


def _process_ingredient_names(item: Item, ingredient_names: list) -> list:
    '''Turn a list of ingredient names into Ingredient objects.'''
    item.ingredients = [
        _get_or_create_ingredient(ingredient_name)
        for ingredient_name in ingredient_names
        # Make sure we don't process any empty strings or None values
        if ingredient_name
    ]
    return item


@api.route('/items/<int:id>')
def get_item(id: int):
    return Item.query.get_or_404(id).serialize()


@api.route('/categories/<int:id>/items', methods=['POST'])
@requires_auth('create:item')
def create_item(payload: dict, id: int):
    '''Create a new item and its ingredients.'''
    category = Category.query.get_or_404(id)
    _verify_ownership(Restaurant, id=category.restaurant_id, auth0_id=payload['sub'])
    # Create new empty item
    new_item = Item()
    # Process ingredients
    if request.get_json().get('ingredients', []):
        new_item = _process_ingredient_names(new_item, request.json['ingredients'])
    # Add remaining data
    data = _prepare_request_data(Item)
    new_item.update(data)

    return {'id': new_item.save()}, 201


@api.route('/items/<int:id>', methods=['PATCH', 'PUT'])
@requires_auth('update:item')
def update_item(payload: dict, id: int):
    category = Category.query.get_or_404(id)
    _verify_ownership(Restaurant, id=category.restaurant_id, auth0_id=payload['sub'])
    # Get existing item
    item = Item.query.get_or_404(id)
    # Process ingredients
    if request.get_json().get('ingredients', []):
        item = _process_ingredient_names(item, request.json['ingredients'])
    # Add remaining data
    data = _prepare_request_data(Item)
    item.update(data)
    item.save()
    return Response(status=200)


@api.route('/items/<int:id>', methods=['DELETE'])
@requires_auth('delete:item')
def delete_item(payload: dict, id: int):
    item = Item.query.get_or_404(id)
    category = Category.query.get_or_404(item.category_id)
    _verify_ownership(Restaurant, id=category.restaurant_id, auth0_id=payload['sub'])
    # Remove children before deletion
    item.ingredients = []
    item.delete()
    return Response(status=200)


@api.route('/ingredients/<int:id>/items')
def get_items_by_ingredient(id: int):
    ingredient = Ingredient.query.get_or_404(id)
    return jsonify([i.serialize() for i in ingredient.items])


### ORDERS ###


def _assert_same_restaurant(items: list) -> bool:
    '''Check if all Item objects in the list are coming from the same restaurant.'''
    # Return false if the list is empty, or if the contained items are not of type Item
    if not items or not all(isinstance(item, Item) for item in items):
        return False
    # Take first item's restaurant_id and compare the rest to that
    restaurant_id = items.pop(0).restaurant_id
    if any(item.restaurant_id != restaurant_id for item in items):
        return False
    return True


def _bulk_fetch_items(item_ids: list) -> list:
    '''Convert a list of item ids to a list of Item objects.'''
    if any(not isinstance(id, int) for id in item_ids):
        abort(400)
    items = [Item.query.get(id) for id in item_ids]
    if not _assert_same_restaurant(items):
        abort(400)
    return items


@api.route('/customers/<int:id>/orders', methods=['POST'])
@requires_auth('create:order')
def create_order(payload: dict, id: int):
    '''Create new order, taking customer_id, restaurant_id and a list of items as item ids.'''
    customer = _verify_ownership(Customer, id, auth0_id=payload['sub'])
    data = _prepare_request_data(Order)
    if data.customer_id != customer.id:
        abort(403)
    new_order = Order()
    if not data.get('items', []):
        abort(400)
    new_order.items = _bulk_fetch_items(data.pop('items'))
    new_order.update(data)
    return {'id': new_order.save()}, 201


@api.route('/customers/<int:id>/orders')
@requires_auth('read:order')
def get_customer_orders(payload: dict, id: int):
    '''Get the customer's order history.'''
    customer = _verify_ownership(Customer, id, auth0_id=payload['sub'])
    return jsonify([o.serialize() for o in customer.orders])


@api.route('/restaurants/<int:id>/orders')
@requires_auth('read:order')
def get_restaurant_orders(payload: dict, id: int):
    '''Get the restaurant's order history.'''
    restaurant = _verify_ownership(Restaurant, id, auth0_id=payload['sub'])
    return jsonify([o.serialize() for o in restaurant.orders])


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
