import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

from src.copycat.database import db

class Text(db.Model):
    __tablename__ = 'texts'
    __table_args__ = {'extend_existing': True}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text_string = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow)

    MAX_TEXT_LENGTH = 3000

    def __init__(self, text_string):
        self.text_string = text_string

    def __repr__(self):
        return f"<Text {self.text_string}>"

    def to_json(self):
        return {
            'id': self.id,
            'text_string': self.text_string,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
    
    @validates('text_string')
    def validate_text(self, key, text_string):
        assert isinstance(text_string, str), "Text must be a string"

        assert len(text_string.strip()) > 0, "Text must be at least one character long"
        assert len(text_string.strip()) <= self.MAX_TEXT_LENGTH, "Text cannot be longer than 3000 characters"
        return text_string