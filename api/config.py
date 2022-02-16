from os import getenv

# Config inspired by:
# https://github.com/miguelgrinberg/flasky/blob/master/config.py


class Config:
    SECRET_KEY = getenv('CLIENT_SECRET')
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH0_AUDIENCE = getenv('AUTH0_AUDIENCE')
    AUTH0_CLIENTID = getenv('AUTH0_CLIENTID')
    AUTH0_DOMAIN = getenv('AUTH0_DOMAIN')
    PAGINATE_RESULTS_PER_PAGE = 10


class TestConfig(Config):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    CUSTOMER_TOKEN = getenv('CUSTOMER_TOKEN')
    RESTAURANT_TOKEN = getenv('RESTAURANT_TOKEN')
