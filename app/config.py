from os import urandom, getenv

class Config:
    ENV = getenv('FLASK_ENV', default='production')
    DEBUG = getenv('FLASK_DEBUG', default=False)
    TESTING = getenv('TESTING', default=False)
    SECRET_KEY = urandom(32)
        
    DB_HOST = getenv('POSTGRES_HOST')
    DB_PORT = getenv('POSTGRES_PORT', 5432)
    DB_NAME = getenv('POSTGRES_DB')
    DB_USER = getenv('POSTGRES_USER')
    DB_PWD  = getenv('POSTGRES_PASSWORD')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    JSON_SORT_KEYS = False

