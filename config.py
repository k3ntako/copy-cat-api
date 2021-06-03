import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class LocalConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/copy_cat')

class TestingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True