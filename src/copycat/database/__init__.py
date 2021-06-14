import sys

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init, upgrade

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    db.init_app(app)
    
    migrate.init_app(app, db)
    
    with app.app_context():
        create_migrations_dir()
        upgrade()

def create_migrations_dir():
    try: 
        init()
    except SystemExit:
        print("Skipping directory migrations initialization...")