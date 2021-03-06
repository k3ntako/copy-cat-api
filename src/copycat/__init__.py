import os

from flask import Flask
from flask_cors import CORS

from src.copycat.controllers import health_check, texts
from src.copycat.database import init_db

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    env_config = os.getenv("APP_CONFIG", "config.LocalConfig")
    app.config.from_object(env_config)
    init_db(app)
    
    CORS(app)
            
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(health_check.bp)
    app.register_blueprint(texts.bp)

    @app.errorhandler(AssertionError)
    def handle_assertion_error(e):
        message = str(e)

        if len(message) == 0:
            message = "Invalid client request parameter"

        return {'error': message}, 400

    return app