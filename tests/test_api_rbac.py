from urllib import response
from api.models import Category, Customer, Restaurant

from conftest import create_app, make_auth_header

app = create_app()

### RESTAURANTS ###


def test_pass_get_restaurants(client):
    response = client.get('/restaurants')
    assert response.status_code == 200
    restaurants = response.get_json()
    assert type(restaurants) == list
    with app.app_context():
        for restaurant in restaurants:
            assert type(restaurant) == dict
            assert type(restaurant['id']) == int
            assert type(restaurant['name']) == str
            assert 'auth0_id' not in restaurant
            assert Restaurant.query.get(restaurant['id']).auth0_id


def test_fail_get_restaurants(client):
    # GET /restaurant (singular instead of plural)
    response = client.get('/restaurant')
    assert response.status_code == 404
    assert response.get_json() is None


def test_pass_get_restaurant(client):
    response = client.get('/restaurants/1')
    assert response.status_code == 200
    assert response.get_json() is not None


def test_fail_get_restaurant(client):
    # Use incorrect ID format
    response = client.get('/restaurants/somestring')
    assert response.status_code == 404


def test_pass_create_restaurant(client):
    new_restaurant_data = {
        "name": "TEST_RESTAURANT",
        "email": "test-restaurant@test.com",
        "phone": "1-234-567890",
        "address": "111 Test St, Test City, RE",
    }
    response = client.post(
        '/restaurants', json=new_restaurant_data, headers=make_auth_header('restaurant')
    )
    assert response.status_code == 201


def test_fail_create_restaurant(client):
    # Try to verify ownership of restaurant resource using customer token
    response = client.post(
        '/restaurants', json={}, headers=make_auth_header('customer')
    )
    assert response.status_code == 403


def test_pass_update_restaurant(client):
    with app.app_context():
        latest_id = max(r.id for r in Restaurant.query.all())
        response = client.patch(
            f'/restaurants/{latest_id}',
            json={'name': 'Renamed Restaurant'},
            headers=make_auth_header('restaurant'),
        )
        assert response.status_code == 200
        restaurant = Restaurant.query.get_or_404(latest_id)
        assert restaurant.name == 'Renamed Restaurant'


def test_fail_update_restaurant(client):
    with app.app_context():
        latest_id = max(r.id for r in Restaurant.query.all())
        response = client.put(
            f'/restaurants/{latest_id}', json={}, headers=make_auth_header('restaurant')
        )
        assert response.status_code == 400


def test_pass_delete_restaurant(client):
    with app.app_context():
        num_restaurants_before = Restaurant.query.count()
        latest_id = max(r.id for r in Restaurant.query.all())
        response = client.delete(
            f'/restaurants/{latest_id}', headers=make_auth_header('restaurant')
        )
        assert response.status_code == 200
        assert num_restaurants_before > Restaurant.query.count()


def test_fail_delete_restaurant(client):
    with app.app_context():
        # Cannot delete all restaurants at once
        response = client.delete('/restaurants')
        assert response.status_code == 405


### CUSTOMERS ###


def test_pass_create_customer(client):
    new_customer_data = {
        "name": "TEST",
        "email": "test@test.com",
        "phone": "1-234-567890",
        "address": "999 Test St, Test City, CU",
    }
    response = client.post(
        '/customers', json=new_customer_data, headers=make_auth_header('customer')
    )
    assert response.status_code == 201


def test_fail_create_customer(client):
    response = client.post('/customers', json={})
    assert response.status_code == 401


def test_pass_get_customer(client):
    with app.app_context():
        latest_id = max(c.id for c in Customer.query.all())
        response = client.get(
            f'/customers/{latest_id}', headers=make_auth_header('customer')
        )
        assert response.status_code == 200
        # Make sure all the data points are present in the response
        assert all(response.json[key] for key in Customer.defaults())


def test_fail_get_customers(client):
    response = client.get('/customers')
    assert response.status_code == 405


def test_pass_update_customer(client):
    with app.app_context():
        latest_id = max(c.id for c in Customer.query.all())
        response = client.patch(
            f'/customers/{latest_id}',
            json={'phone': '987-654-321'},
            headers=make_auth_header('customer'),
        )
        assert response.status_code == 200
        customer = Customer.query.get_or_404(latest_id)
        assert customer.phone == '987-654-321'


def test_fail_update_customer(client):
    with app.app_context():
        latest_id = max(c.id for c in Customer.query.all())
        response = client.patch(
            f'/customers/{latest_id}',
            json={'phone': None},
            headers=make_auth_header('customer'),
        )
        assert response.status_code == 400


def test_pass_delete_customer(client):
    with app.app_context():
        num_customers_before = Customer.query.count()
        latest_id = max(c.id for c in Customer.query.all())
        response = client.delete(
            f'/customers/{latest_id}', headers=make_auth_header('customer')
        )
        assert response.status_code == 200
        assert num_customers_before > Customer.query.count()


def test_fail_delete_customer(client):
    with app.app_context():
        # Cannot delete all customers at once
        response = client.delete('/customers')
        assert response.status_code == 405


### CATEGORIES ###


def test_pass_create_category(client):
    response = client.post(
        '/restaurants/1/categories',
        json={'name': 'Tastiest'},
        headers=make_auth_header('restaurant'),
    )
    assert response.status_code == 201


def test_fail_create_category(client):
    response = client.post(
        '/restaurants/1/categories',
        json={'name': 'Yummies'},
        headers=make_auth_header('customer'),
    )
    assert response.status_code == 403


def test_pass_update_category(client):
    with app.app_context():
        latest_id = max(c.id for c in Category.query.all())
        response = client.patch(
            f'/categories/{latest_id}',
            json={'name': 'Yummies'},
            headers=make_auth_header('restaurant'),
        )
        assert response.status_code == 200
        assert Category.query.get_or_404(latest_id).name == 'Yummies'


def test_fail_update_category(client):
    with app.app_context():
        latest_id = max(c.id for c in Category.query.all())
        response = client.put(
            f'/categories/{latest_id}',
            json={'blame': 'Yummies'},
            headers=make_auth_header('restaurant'),
        )
        assert response.status_code == 400


def test_pass_delete_category(client):
    with app.app_context():
        latest_id = max(c.id for c in Category.query.all())
        response = client.delete(
            f'/categories/{latest_id}',
            headers=make_auth_header('restaurant'),
        )
        assert response.status_code == 200


def test_fail_delete_category(client):
    with app.app_context():
        latest_id = max(c.id for c in Category.query.all())
        response = client.delete(
            f'/categories/{latest_id}',
            headers=make_auth_header('customer'),
        )
        assert response.status_code == 403


### ITEMS AND INGREDIENTS ###


def test_pass_search_items(client):
    response = client.post('/items', json={'search_term': 'soup'})
    assert response.status_code == 200
    assert len(response.json) >= 1


def test_fail_search_items(client):
    # Invalid request format
    response = client.post('/items', data={'search_term': 'soup'})
    assert response.status_code == 400


def test_pass_get_item(client):
    response = client.get('/items/1')
    assert response.status_code == 200
    assert 'name' in response.json
    assert 'price' in response.json



def test_fail_get_item(client):
    # Singular resource in URL
    response = client.get('/item/1')
    assert response.status_code == 404


def test_pass_create_item(client):
    pass


def test_fail_create_item(client):
    pass


def test_pass_update_item(client):
    pass


def test_fail_update_item(client):
    pass


def test_pass_delete_item(client):
    pass


def test_fail_delete_item(client):
    pass


def test_pass_get_items_by_ingredient(client):
    for ingredient_id in {1, 23, 57}:
        response = client.get(f'/ingredients/{ingredient_id}/items')
        assert response.status_code == 200
        assert response.json


def test_fail_get_items_by_ingredient(client):
    for ingredient_name in {'turmeric', 'saffron', 'pepper'}:
        response = client.get(f'/ingredients/{ingredient_name}/items')
        assert response.status_code == 404


### ORDERS ###


def test_pass_create_order(client):
    orders = [
        {'items': [1, 2, 3, 4]},
        {'items': [44, 45, 46, 47, 48]},
        {'items': [87, 88, 89]},
    ]
    for order in orders:
        response = client.post(
            '/customers/1/orders', json=order, headers=make_auth_header('customer')
        )
        assert response.status_code == 201


def test_fail_create_order(client):
    # Mix up items from different restaurants per order
    orders = [
        {'items': [93, 2, 75, 4]},
        {'items': [23, 45, 1, 6]},
        {'items': [52, 2, 43]},
    ]
    for order in orders:
        response = client.post(
            '/customers/2/orders', json=order, headers=make_auth_header('customer')
        )
        assert response.status_code == 400


def test_pass_get_customer_orders(client):
    response = client.get('/customers/1/orders', headers=make_auth_header('customer'))
    assert response.status_code == 200
    assert len(response.json) >= 3


def test_fail_get_customer_orders(client):
    # Mix up resources in the URL
    response = client.get('/orders/1/customer', headers=make_auth_header('customer'))
    assert response.status_code == 404


def test_pass_get_restaurant_orders(client):
    response = client.get(
        '/restaurants/1/orders', headers=make_auth_header('restaurant')
    )
    assert response.status_code == 200
    assert len(response.json) >= 1
    assert response.json[0]['customer_id'] == 1


def test_fail_get_restaurant_orders(client):
    # Mix up resources in the URL
    response = client.get(
        '/orders/1/restaurant', headers=make_auth_header('restaurant')
    )
    assert response.status_code == 404
