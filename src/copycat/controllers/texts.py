from flask import Blueprint, request, jsonify

from src.copycat.database import db
from src.copycat.database.models.text import Text

bp = Blueprint("texts", __name__, url_prefix="/api/texts")

@bp.route('', methods=['POST'])
def text_upload():
    assert request.is_json, 'Request body must be a JSON'
    assert 'text_string' in request.json, '"text_string" parameter is required'

    text = Text(request.json['text_string'])
    db.session.add(text)
    db.session.commit()
    
    return text.to_json(), 201