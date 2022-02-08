from os import getenv, urandom

# Config inspired by:
# https://github.com/miguelgrinberg/flasky/blob/master/config.py


class Config:
    SECRET_KEY = getenv('SECRET_KEY', urandom(16))
    SQLALCHEMY_DATABASE_URI = getenv('DBURI', 'postgresql:///jalapino')
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Keeping for future reference

    RESULTS_PER_PAGE = 10


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv('DBURI_TEST', 'postgresql:///jalapino_test')
    TESTING = True
    WTF_CSRF_ENABLED = False
