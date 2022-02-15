from api.models import Restaurant

from conftest import create_app, make_auth_header

app = create_app()


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
    response = client.patch(
        '/restaurants/1',
        json={'name': 'Renamed Restaurant'},
        headers=make_auth_header('restaurant'),
    )
    assert response.status_code == 200
    with app.app_context():
        restaurant = Restaurant.query.get_or_404(1)
        assert restaurant.name == 'Renamed Restaurant'


def test_fail_update_restaurant(client):
    response = client.put(
        '/restaurants/1', json={}, headers=make_auth_header('restaurant')
    )
    assert response.status_code == 400


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


def test_fail_get_customers(client):
    response = client.get('/customers')
    assert response.status_code == 405
