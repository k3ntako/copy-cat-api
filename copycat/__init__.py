import os

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func

import config

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    env_config = os.getenv("APP_SETTINGS", "config.LocalConfig")
    app.config.from_object(env_config)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    class TextModel(db.Model):
        __tablename__ = 'texts'

        id = db.Column(db.Integer, primary_key=True)
        text_string = db.Column(db.String())
        created_date = db.Column(db.DateTime, default=func.now())
        time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now(), default=func.now())

        def __init__(self, text_string):
            print(text_string)
            self.text_string = text_string

        def __repr__(self):
            return f"<Text {self.text_string}>"

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/health')
    def health_check():
        return {"status": "UP"}


    return app