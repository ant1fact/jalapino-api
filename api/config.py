from os import getenv

# Config inspired by:
# https://github.com/miguelgrinberg/flasky/blob/master/config.py


class Config:
    SECRET_KEY = getenv('CLIENT_SECRET')
    SQLALCHEMY_DATABASE_URI = getenv(
        'SQLALCHEMY_DATABASE_URI',
        # If SQLALCHEMY_DATABASE_URI is not found,
        # take the path from DATABASE_URL, but replace the scheme
        # as SQLAlchemy requires it to be postgresql instead of postgres
        getenv('DATABASE_URL').replace('postgres:', 'postgresql:')
    )
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
