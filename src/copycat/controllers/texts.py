from flask import Blueprint, request, jsonify

from src.copycat.database import db
from src.copycat.database.models.text import Text

bp = Blueprint("texts", __name__, url_prefix="/api/texts")

@bp.route('', methods=['POST'])
def text_upload():
    text = Text(request.json['text_string'])
    db.session.add(text)
    db.session.commit()
    
    return text.to_json(), 201