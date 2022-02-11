import json
import re

from flask import Blueprint, Response, abort, jsonify, request, session
from werkzeug.exceptions import HTTPException

from .auth import AuthError, requires_auth

api = Blueprint('api', __name__)

from .config import Config
from .models import Category, Customer, Ingredient, Item, Order, Restaurant


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


### API INFO ###


@api.route('/')
def root():
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


### RESTAURANTS ###


@api.route('/restaurants')
def get_restaurants():
    '''Return a list of all restaurants with active status paginated.'''
    page = request.args.get('page', 1, type=int)
    restaurants = (
        Restaurant.query.filter_by(is_active=True)
        .paginate(page=page, per_page=Config.PAGINATE_RESULTS_PER_PAGE)
        .items
    )
    return jsonify([r.serialize() for r in restaurants])


@api.route('/restaurants/<int:id>')
def get_restaurant(id: int):
    return Restaurant.query.get_or_404(id).serialize()


@api.route('/restaurants', methods=['POST'])
@requires_auth('create:restaurant')
def create_restaurant(payload: dict):
    '''Create a restaurant resource once per auth0 restaurant registration.'''
    # If requester's auth0 id already exists, return the associated resource instead
    restaurant = Restaurant.query.filter_by(auth0_id=payload['sub']).first()
    if restaurant is not None:
        return get_restaurant(restaurant.id), 302
    # Create empty resource, add data and save to DB
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
@requires_auth('admin')
def delete_restaurant(id: int):
    '''Admin delete a restaurant record that has been deactivated by its owner.'''
    restaurant = Restaurant.query.get_or_404(id)
    if restaurant.is_active:
        abort(409)
    restaurant.delete()
    return Response(status=200)


### CUSTOMERS ###


@api.route('/customers')
@requires_auth('admin')
def get_customers():
    '''Return a list of all customers paginated.
    NOTE: For data protection, this endpoint is only available to admins.'''
    page = request.args.get('page', 1, type=int)
    customers = Customer.query.paginate(
        page=page, per_page=Config.PAGINATE_RESULTS_PER_PAGE
    ).items
    return jsonify([c.serialize() for c in customers])


@api.route('/customers/<int:id>')
@requires_auth('read:customer')
def get_customer(payload: dict, id: int):
    customer = _verify_ownership(Customer, id, auth0_id=payload['sub'])
    return customer.serialize()


@api.route('/customers', methods=['POST'])
@requires_auth('create:customer')
def create_customer(payload: dict):
    '''Create a customer resource once per auth0 customer registration.'''
    # If requester's auth0 id already exists, return the associated resource instead
    customer = Customer.query.filter_by(auth0_id=payload['sub']).first()
    if customer is not None:
        return customer.serialize(), 302
    # Create empty resource, add data and save to DB
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
@requires_auth('admin')
def delete_customer(id: int):
    '''Admin delete a customer record that has been deactivated by its owner.'''
    customer = Customer.query.get_or_404(id)
    if customer.is_active:
        abort(409)
    customer.delete()
    return Response(status=200)


### CATEGORIES ###


@api.route('/restaurants/<int:id>/categories')
def get_restaurant_categories(id: int):
    '''Get all categories specific to a restaurant.'''
    return jsonify([c.serialize() for c in Restaurant.query.get_or_404(id).categories])


@api.route('/restaurants/<int:id>/categories', methods=['POST'])
@requires_auth('create:category')
def create_category(payload: dict, id: int):
    '''Create new category under the parent restaurant resource.'''
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
    category.items = []
    category.delete()
    return Response(status=200)


### ITEMS AND INGREDIENTS ###


@api.route('/items')
def get_items():
    '''Return a list of all items paginated.'''
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(
        page=page, per_page=Config.PAGINATE_RESULTS_PER_PAGE
    ).items
    return jsonify([i.serialize() for i in items])


@api.route('/items/<int:id>')
def get_item(id: int):
    return Item.query.get_or_404(id).serialize()


def _get_or_create_ingredient(ingredient_name: str) -> Ingredient:
    '''Helper function for create_item endpoint.'''
    ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
    if ingredient is not None:
        return ingredient
    new_ingredient = Ingredient(name=ingredient_name)
    new_ingredient.save()
    return new_ingredient


def _process_ingredients(item: Item, ingredients: list) -> list:
    '''Turn a list of ingredient dicts {'name': '...'} into Ingredient objects.'''
    try:
        item.ingredients = [
            _get_or_create_ingredient(ingredient['name'])
            for ingredient in ingredients
            # Make sure we don't process any empty strings or None values
            if ingredient['name']
        ]
        return item
    except KeyError:
        abort(400)


@api.route('/categories/<int:id>/items', methods=['POST'])
@requires_auth('create:item')
def create_item(payload: dict, id: int):
    '''Create a new item and its ingredients.'''
    category = Category.query.get_or_404(id)
    _verify_ownership(Restaurant, id=category.restaurant_id, auth0_id=payload['sub'])
    # Create new empty item
    new_item = Item()
    if request.get_json().get('ingredients', []):
        new_item = _process_ingredients(new_item, request.json['ingredients'])
    data = _prepare_request_data(Item)
    # Add remaining data
    new_item.update(data)

    return {'id': new_item.save()}, 201


@api.route('/items/<int:id>', methods=['PATCH', 'PUT'])
@requires_auth('update:item')
def update_item(payload: dict, id: int):
    category = Category.query.get_or_404(id)
    _verify_ownership(Restaurant, id=category.restaurant_id, auth0_id=payload['sub'])
    # Get existing item
    item = Item.query.get_or_404(id)
    if request.get_json().get('ingredients', []):
        item = _process_ingredients(item, request.json['ingredients'])
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


@api.route('/ingredients')
def get_ingredients():
    return jsonify([i.serialize() for i in Ingredient.query.all()])


@api.route('/ingredients/<int:id>')
def get_ingredient(id: int):
    return Ingredient.query.get_or_404(id).serialize()


@api.route('/ingredients/<int:id>', methods=['DELETE'])
@requires_auth('admin')
def delete_ingredient(id: int):
    ingredient = Ingredient.query.get_or_404(id)
    ingredient.delete()
    return Response(status=200)


@api.route('/ingredients/<int:id>/items')
def get_items_by_ingredient(id: int):
    ingredient = Ingredient.query.get_or_404(id)
    return jsonify([i.serialize() for i in ingredient.items])


### ORDERS ###


@api.route('/orders')
@requires_auth('admin')
def get_orders():
    '''Get all past orders paginated.'''
    return jsonify([o.serialize() for o in Order.query.all()])


def _initialize_basket():
    if 'basket' not in session:
        session['basket'] = {'restaurant_id': int, 'customer_id': int, 'item_ids': []}


@api.route('/customers/<int:id>/basket', methods=['POST'])
@requires_auth('create:order')
def add_item_to_basket(payload: dict, id: int):
    '''Add a new item to the session basket.
    Expects ?restaurant_id=<id>&item_id=<id> in the query parameters.'''
    if 'restaurant_id' not in request.args or 'item_id' not in request.args:
        abort(400)
    customer = _verify_ownership(Customer, id, auth0_id=payload['sub'])
    _initialize_basket()
    basket = session['basket']
    if not basket['customer_id']:
        basket['customer_id'] = customer.id
    elif basket['customer_id'] != customer.id:
        abort(403)
    if not basket['restaurant_id']:
        basket['restaurant_id'] = request.args['restaurant_id']
    elif basket['restaurant_id'] != request.args['restaurant_id']:
        abort(409)
    basket['item_ids'].append(request.args['item_id'])
    session.modified = True
    return Response(status=200)


@api.route('/customers/<int:id>/basket')
@requires_auth('read:order')
def get_items_from_basket(payload: dict, id: int):
    _verify_ownership(Customer, id, auth0_id=payload['sub'])
    _initialize_basket()
    return jsonify(
        [Item.query.get_or_404(id).serialize() for id in session['basket']['item_ids']]
    )


@api.route('/customers/<int:id>/orders', methods=['POST'])
@requires_auth('create:order')
def submit_order(payload: dict, id: int):
    customer = _verify_ownership(Customer, id, auth0_id=payload['sub'])
    # Check if basket is empty
    basket = session['basket']
    if not basket['item_ids']:
        abort(422)
    new_order = Order()
    new_order.customer_id = basket['customer_id']
    new_order.restaurant_id = basket['restaurant_id']
    new_order.items = [Item.query.get_or_404(item_id) for item_id in basket['item_ids']]

    return {'id': new_order.save()}, 201


@api.route('/customers/<int:id>/orders')
@requires_auth('read:order')
def get_customer_orders(payload: dict, id: int):
    '''Get a customer's order history.'''
    customer = _verify_ownership(Customer, id, auth0_id=payload['sub'])
    return jsonify([o.serialize() for o in customer.orders])


@api.route('/restaurants/<int:id>/orders')
@requires_auth('read:order')
def get_restaurant_orders(payload: dict, id: int):
    '''Get a restaurant's order history.'''
    restaurant = _verify_ownership(Restaurant, id, auth0_id=payload['sub'])
    return jsonify([o.serialize() for o in restaurant.orders])


@api.route('/orders/<int:id>', methods=['DELETE'])
@requires_auth('admin')
def delete_order(id: int):
    order = Order.query.get_or_404(id)
    order.delete()
    return Response(status=200)


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
