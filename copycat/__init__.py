import os

from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    env_config = os.getenv("APP_CONFIG", "config.LocalConfig")
    app.config.from_object(env_config)
    db.init_app(app)
    migrate.init_app(app, db)  

    class TextModel(db.Model):
        __tablename__ = 'texts'

        id = db.Column(db.Integer, primary_key=True)
        text_string = db.Column(db.String())
        created_at = db.Column(db.DateTime, default=func.now())
        updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), default=func.now())

        def __init__(self, text_string):
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

    @app.route('/api/texts', methods=['POST', 'GET'])
    def handle_cars():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_text = TextModel(text_string=data['text_string'])
                db.session.add(new_text)
                db.session.commit()
                return {"message": f"Added: \"{new_text.text_string}\"."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':
            texts = TextModel.query.all()
            results = [
                {
                    "text_string": text.text_string,
                } for text in texts]

            return {"count": len(results), "texts": results}


    return app