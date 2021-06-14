from flask import Blueprint, request, jsonify
from sqlalchemy import desc

from src.copycat.database import db
from src.copycat.database.models.text import Text

bp = Blueprint("texts", __name__, url_prefix="/api/texts")

@bp.route('', methods=['GET'])
def list_texts():
    texts = Text.query.order_by(desc(Text.created_at)).limit(10).all()
    texts_list = [text_entry.to_json() for text_entry in texts]

    return jsonify(texts_list), 200

@bp.route('', methods=['POST'])
def text_upload():
    assert request.is_json, 'Request body must be a JSON'
    assert 'text_string' in request.json, '"text_string" parameter is required'

    text = Text(request.json['text_string'])
    db.session.add(text)
    db.session.commit()
    
    return text.to_json(), 201
