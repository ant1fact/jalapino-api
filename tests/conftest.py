import pytest
from api import create_app
from api.config import TestConfig

def make_auth_header(role: str) -> str:
    assert role in {'customer', 'restaurant'}
    tokens = {
        'customer': TestConfig.CUSTOMER_TOKEN,
        'restaurant': TestConfig.RESTAURANT_TOKEN
    }
    return {'Authorization': f'Bearer {tokens[role]}'}


@pytest.fixture()
def app():  # sourcery skip: inline-immediately-yielded-variable
    app = create_app(config=TestConfig)
    
    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()