import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    dialect = "postgresql"
    driver = "psycopg2"
    user = os.getenv('RDS_USERNAME')
    password = os.getenv('RDS_PASSWORD')
    hostname = os.getenv('RDS_HOSTNAME')
    port = os.getenv('RDS_PORT')
    db_name = os.getenv('RDS_DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'{dialect}+{driver}://{user}:{password}@{hostname}:{port}/{db_name}'
    print(f'SQLALCHEMY_DATABASE_URI!! {SQLALCHEMY_DATABASE_URI}')

class LocalConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql+psycopg2://postgres:postgres@localhost:5432/copy_cat')

class TestingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True