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

    def __init__(self, text_string):
        self.text_string = text_string

    def __repr__(self):
        return f"<Text {self.text_string}>"

