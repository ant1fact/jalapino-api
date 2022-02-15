from api.models import Restaurant
from conftest import create_app

app = create_app()

def test_pass_get_restaurants(client):
    response = client.get('/restaurants')
    assert response.status_code == 200    
    restaurants = response.get_json()

    assert len(restaurants) == 3
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
    restaurant = response.get_json()

    assert restaurant['name'] == 'Not Necessarily BBQ'
    assert restaurant['website'] == 'www.nn-bbq.com'
    assert len(restaurant['categories']) == 4
    with app.app_context():
        assert Restaurant.query.get(1).categories[0].items[0].ingredients

def test_fail_get_restaurant(client):
    response = client.get('/restaurants/somestring')
    assert response.status_code == 404

def test_pass_create_customer(client):
    new_customer_data = {
        "name": "TEST",
        "email": "test@test.com",
        "phone": "1-234-567890",
        "address": "999 Test St, Test City, TE"
    }
    response = client.post('/customers', json={}})
    assert response.status_code == 401

def test_fail_create_customer(client):
    new_customer_data = {
        "name": "TEST",
        "email": "test@test.com",
        "phone": "1-234-567890",
        "address": "999 Test St, Test City, TE"
    }
    response = client.post('/customers', json={}})
    assert response.status_code == 401

def test_fail_get_customers(client):
    response = client.get('/customers')
    assert response.status_code == 405