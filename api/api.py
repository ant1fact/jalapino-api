import json

from flask import Blueprint, Response, abort, jsonify, request, session
from werkzeug.exceptions import HTTPException

from .auth import AuthError, requires_auth

api = Blueprint('api', __name__)

from .config import Config
from .models import Category, Customer, Ingredient, Item, Order, Restaurant


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
def create_restaurant(payload):
    '''Create a restaurant resource once per auth0 restaurant registration.'''
    # If requester's auth0 id already exists, return the associated resource instead
    restaurant = Restaurant.query.filter_by(auth0_id=payload['sub']).first()
    if restaurant is not None:
        return get_restaurant(restaurant.id), 302
    # Get request body and attach auth0 id from payload
    body = request.get_json()
    body['auth0_id'] = payload['sub']
    # Make sure request body contains data for non-nullable columns in the DB
    for field in Restaurant.required_fields(method='POST'):
        field_data = body.get(field, None)
        if field_data in {'', None}:
            abort(400)
    # Create empty resource, add data from request body and save to DB
    new_restaurant = Restaurant()
    new_restaurant.update(body)
    new_restaurant.save()

    return {'id': new_restaurant.id}, 201


@api.route('/restaurants/<int:id>', methods=['PATCH'])
@requires_auth('update:restaurant')
def update_restaurant(payload: dict, id: int):
    restaurant = Restaurant.get_or_404(id)
    # Check that requester is the owner of the resource
    if restaurant.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    restaurant.update(body)
    restaurant.save()
    return Response(status=200)


@api.route('/restaurants/<int:id>', methods=['DELETE'])
@requires_auth('admin')
def delete_restaurant(id: int):
    restaurant = Restaurant.query.get_or_404(id)
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
    customer = Customer.query.get_or_404(id)
    if customer.auth0_id != payload['sub']:
        abort(403)
    return Customer.query.get_or_404(id).serialize()


@api.route('/customers', methods=['POST'])
@requires_auth('create:customer')
def create_customer(payload):
    '''Create a customer resource once per auth0 customer registration.'''
    # If requester's auth0 id already exists, return the associated resource instead
    customer = Customer.query.filter_by(auth0_id=payload['sub']).first()
    if customer is not None:
        return get_customer(payload, customer.id), 302
    # Get request body and attach auth0 id from payload
    body = request.get_json()
    body['auth0_id'] = payload['sub']
    # Make sure request body contains data for non-nullable columns in the DB
    for field in Customer.required_fields(method='POST'):
        field_data = body.get(field, None)
        if field_data in {'', None}:
            abort(400)
    # Create empty resource, add data from request body and save to DB
    new_customer = Customer()
    new_customer.update(body)
    new_customer.save()

    return {'id': new_customer.id}, 201


@api.route('/customers/<int:id>', methods=['PATCH'])
@requires_auth('update:customer')
def update_customer(payload: dict, id: int):
    customer = Customer.get_or_404(id)
    # Check that requester is the owner of the resource
    if customer.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    customer.update(body)
    customer.save()
    return Response(status=200)


@api.route('/customers/<int:id>', methods=['DELETE'])
@requires_auth('admin')
def delete_customer(id: int):
    customer = Customer.query.get_or_404(id)
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
    restaurant = Restaurant.get_or_404(id)
    if restaurant.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    # Require minimum information for creating a new category
    if body.get('restaurant_id', 0) != restaurant.id or not body.get('name', ''):
        abort(400)
    # Create new category
    new_category = Category()
    new_category.update(body)
    new_category.save()
    # Bind new category to parent restaurant
    restaurant.categories.append(new_category)
    restaurant.save()
    return {'id': new_category.id}, 201


### ITEMS AND INGREDIENTS ###


@api.route('/items')
def get_items():
    '''Return a list of all items paginated.'''
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(
        page=page, per_page=Config.PAGINATE_RESULTS_PER_PAGE
    ).items
    return jsonify([i.serialize() for i in items])


def get_or_create_ingredient(ingredient_name: str) -> Ingredient:
    '''Helper function for create_item endpoint.'''
    ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
    if ingredient is not None:
        return ingredient
    new_ingredient = Ingredient(name=ingredient_name)
    new_ingredient.save()
    return new_ingredient


@api.route('/categories/<int:id>/items', methods=['POST'])
@requires_auth('create:item')
def create_item(payload: dict, id: int):
    '''Create a new item and its ingredients.'''
    category = Category.query.get_or_404(id)
    restaurant = Restaurant.query.get_or_404(category.restaurant_id)
    # Validate ownership of data
    if restaurant.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    # Set item's parent ID
    body['category_id'] = id
    for field in Item.required_fields(method='POST'):
        field_data = body.get(field, None)
        if field_data in {'', None}:
            abort(400)
    new_item = Item()
    # First take care of converting any ingredient names to ingredient objects
    if body.get('ingredients', []):
        # Remove original ingredients list from message body using .pop()
        # so it doesn't revert when calling .update() on new_item
        new_item.ingredients = [
            get_or_create_ingredient(ingredient_name)
            for ingredient_name in body.pop('ingredients')
        ]
    # Add remaining data to transient Item record
    new_item.update(body)
    new_item.save()

    return {'id': new_item.id}, 201


@api.route('/items/<int:id>', methods=['PATCH', 'PUT'])
@requires_auth('update:item')
def update_item(payload: dict, id: int):
    category = Category.query.get_or_404(id)
    restaurant = Restaurant.query.get_or_404(category.restaurant_id)
    # Validate ownership of data
    if restaurant.auth0_id != payload['sub']:
        abort(403)
    body = request.get_json()
    item = Item.query.get_or_404(id)
    # -- PREFLIGHT PUT --
    if request.method == 'PUT':
        for field in Item.required_fields(method='PUT'):
            if field not in body:
                abort(400)
    # -- PERFORM PUT / PATCH --
    # Take care of the item.ingredients list first
    if body.get('ingredients', []):
        try:
            # Remove original ingredients list from message body using .pop() so it won't
            # override the fetched Ingredient records when calling .update() on new_item
            item.ingredients = [
                get_or_create_ingredient(ingredient_name)
                for ingredient_name in body.pop('ingredients')
            ]
        except Exception as e:
            api.logger.error(e)
            abort(400)
    # Replace remaining data on the item being updated
    item.update(body)
    item.save()
    return Response(status=200)


@api.route('/items/<int:id>', methods=['DELETE'])
@requires_auth('delete:item')
def delete_item(payload: dict, id: int):
    item = Item.query.get_or_404(id)
    category = Category.query.get_or_404(item.category_id)
    restaurant = Restaurant.query.get_or_404(category.restaurant_id)
    # Validate ownership of data
    if restaurant.auth0_id != payload['sub']:
        abort(403)
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


@api.route('/customers/<int:id>/basket', methods=['POST'])
@requires_auth('create:order')
def add_item_to_basket(payload: dict, id: int):
    customer = Customer.query.get_or_404(id)
    if customer.auth0_id != payload['sub']:
        abort(403)
    item_id = request.args.get('item_id', None)
    if item_id is None:
        abort(400)
    session['basket'].append(item_id)
    return Response(status=200)


@api.route('/customers/<int:id>/basket')
@requires_auth('read:order')
def get_items_from_basket(payload: dict, id: int):
    customer = Customer.query.get_or_404(id)
    if customer.auth0_id != payload['sub']:
        abort(403)
    return jsonify([Item.query.get_or_404(id).serialize() for id in session['basket']])


@api.route('/customers/<int:id>/orders', methods=['POST'])
@requires_auth('create:order')
def submit_order(payload: dict, id: int):
    customer = Customer.query.get_or_404(id)
    if customer.auth0_id != payload['sub']:
        abort(403)
    if not session['basket']:
        abort(422)
    new_order = Order()
    # TODO add items from session & customer/restaurant IDs to new_order
    new_order.save()
    return {'id': new_order.id}, 201


@api.route('/customers/<int:id>/orders')
@requires_auth('read:order')
def get_customer_orders(payload: dict, id: int):
    '''Get a customer's order history.'''
    customer = Customer.query.get_or_404(id)
    if customer.auth0_id != payload['sub']:
        abort(403)
    return jsonify([o.serialize() for o in customer.orders])


@api.route('/restaurants/<int:id>/orders')
@requires_auth('read:order')
def get_restaurant_orders(payload: dict, id: int):
    '''Get a restaurant's order history.'''
    restaurant = Restaurant.query.get_or_404(id)
    if restaurant.auth0_id != payload['sub']:
        abort(403)
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
