class Config(object):
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = "this-is-secret-key-can-change-it"
    DB_HOST = "mongodb://localhost:27017/"

class ProductionConfig(Config):
    DB_HOST = "mongodb://db:27017/"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True