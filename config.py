import os
import json

from src.utilities.encrypt_secrets import decrypt_secrets
from src.utilities.file_io import FileIO

class Config:
    DEBUG = False
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SECRETS_PATH = "./encrypted-secrets-prod"
    if os.getenv('SECRETS_KEY'):
        secretsJsonStr = decrypt_secrets(FileIO(), SECRETS_PATH, os.getenv('SECRETS_KEY'))
        secretsJson = json.loads(secretsJsonStr)
        
        dialect = "postgresql"
        driver = "psycopg2"
        user = secretsJson['RDS_USERNAME']
        password = secretsJson['RDS_PASSWORD']
        hostname = secretsJson['RDS_HOSTNAME']
        port = secretsJson['RDS_PORT']
        db_name = secretsJson['RDS_DB_NAME']

        SQLALCHEMY_DATABASE_URI = f'{dialect}+{driver}://{user}:{password}@{hostname}:{port}/{db_name}'

class LocalConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql+psycopg2://postgres:postgres@localhost:5432/copy_cat')

class TestingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql+psycopg2://postgres:postgres@localhost:5432/copy_cat_testing')
