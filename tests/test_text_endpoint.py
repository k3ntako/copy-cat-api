from flask import json

from src.copycat.database import db
from src.copycat.database.models.text import Text
    

def test_post_returns_created_text(client):
    """POST text endpoint should return the newly created text"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict(text_string='test string 1')),
        content_type='application/json'
    ) 
    
    assert res.status == '201 CREATED'
    assert res.json['text_string'] == 'test string 1'
    assert isinstance(res.json['id'], str)
    assert isinstance(res.json['created_at'], str)
    assert isinstance(res.json['updated_at'], str)

def test_post_commits_to_db(app, client):
    """POST text endpoint should commit text to database"""
    client.post(
        '/api/texts',
        data=json.dumps(dict(text_string='test string 2')),
        content_type='application/json'
    ) 

    with app.app_context():
        text_row = db.session.query(Text).filter_by(text_string='test string 2').first()
        assert text_row.text_string == 'test string 2'

def test_post_rejects_empty_string(app, client):
    """POST text endpoint should not allow empty strings"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict(text_string='')),
        content_type='application/json'
    ) 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == "Text must be at least one character long"

def test_post_rejects_only_whitespace(app, client):
    """POST text endpoint should not allow string with only whitespace"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict(text_string=' \n \n ')),
        content_type='application/json'
    ) 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == "Text must be at least one character long"

def test_post_only_allows_strings(app, client):
    """POST text endpoint should not allow text_string parameter that is not a string"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict(text_string=1)),
        content_type='application/json'
    ) 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == "Text must be a string"

def test_post_validates_length(app, client):
    """POST text endpoint should not allow text longer than the limit"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict(text_string="x" * 251)),
        content_type='application/json'
    ) 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == "Text cannot be longer than 250 characters"
