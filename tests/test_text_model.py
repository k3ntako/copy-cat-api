from datetime import datetime
import uuid

from flask import request

import pytest

from src.copycat.database import db
from src.copycat.database.models.text import Text

def test_text_model_validates_type():
    """Text model should only allow string for text_string parameter"""
    with pytest.raises(AssertionError, match='Text must be a string'):
        Text(None)
  
def test_text_model_rejects_empty_string():
    """Text model should reject empty string for text_string"""
    with pytest.raises(AssertionError, match='Text must be at least one character long'):
        Text('')
    
def test_text_model_rejects_whitespace():
    """Text model should reject whitespace for text_string"""
    with pytest.raises(AssertionError, match='Text must be at least one character long'):
        Text('\n')

def test_text_model_rejects_multiple_whitespace():
    """Text model should reject multiple whitespaces for text_string"""
    with pytest.raises(AssertionError, match='Text must be at least one character long'):
        Text('   \n \n  ')

def test_text_max_length():
    """Text model should have a max text length"""
    assert Text.MAX_TEXT_LENGTH == 250

def test_text_model_allows_text_at_max_length():
    """Text model should allow text_string with max text length"""
    text = Text('x' * Text.MAX_TEXT_LENGTH)
    assert len(text.text_string) == Text.MAX_TEXT_LENGTH

def test_text_model_rejects_text_over_max_length():
    """Text model should reject text_string longer than max text length"""
    with pytest.raises(AssertionError, match='Text cannot be longer than 250 characters'):
        Text('x' * (Text.MAX_TEXT_LENGTH + 1))

def test_text_defaults(app):
    """Text model set defaults for ID and dates when committing to database"""
    text = Text('String for text?')

    with app.app_context():
        db.session.add(text)
        db.session.commit()

        assert isinstance(text.id, uuid.UUID)
        assert text.text_string == 'String for text?'
        assert isinstance(text.created_at, datetime)
        assert isinstance(text.updated_at, datetime)

def test_text_to_json(app):
    """Text model should serialize text instance to JSON"""
    text = Text('Test text!')

    with app.app_context():
        db.session.add(text)
        db.session.commit()

        json = text.to_json()
        assert json['id'] == text.id
        assert json['text_string'] == 'Test text!'
        assert json['created_at'] == text.created_at.isoformat()
        assert json['updated_at'] == text.updated_at.isoformat()

def test_text_model_accepts_multiline_string(app):
    """Text model should accept multiline texts"""
    text = Text('\nTest text!\n\nhello\n ')

    with app.app_context():
        db.session.add(text)
        db.session.commit()

        assert text.text_string == '\nTest text!\n\nhello\n '

