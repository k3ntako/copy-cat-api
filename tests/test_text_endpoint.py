from flask import json

import pytest

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

def test_post_rejects_request_without_json_body(client):
    """POST text endpoint should not allow requests without a JSON body"""
    res = client.post('/api/texts') 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == 'Request body must be a JSON'

def test_post_rejects_request_without_text_string_paramter(client):
    """POST text endpoint should require text_string parameter"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict()),
        content_type='application/json'
    ) 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == '"text_string" parameter is required'

def test_post_rejects_empty_string(client):
    """POST text endpoint should not allow empty strings"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict(text_string='')),
        content_type='application/json'
    ) 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == "Text must be at least one character long"

def test_post_rejects_only_whitespace(client):
    """POST text endpoint should not allow string with only whitespace"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict(text_string=' \n \n ')),
        content_type='application/json'
    ) 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == "Text must be at least one character long"

def test_post_only_allows_strings(client):
    """POST text endpoint should not allow text_string parameter that is not a string"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict(text_string=1)),
        content_type='application/json'
    ) 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == "Text must be a string"

def test_post_validates_length(client):
    """POST text endpoint should not allow text longer than the limit"""
    res = client.post(
        '/api/texts',
        data=json.dumps(dict(text_string="x" * 251)),
        content_type='application/json'
    ) 
    
    assert res.status == '400 BAD REQUEST'
    assert res.json['error'] == "Text cannot be longer than 250 characters"

def test_get_returns_empty_array_when_no_texts_in_db(client):
    """GET text endpoint should return empty array if no texts exist"""
    res = client.get('/api/texts') 
    
    assert res.status == '200 OK'
    assert res.json == []

@pytest.mark.parametrize('texts', [1], indirect=True)
def test_get_returns_text_from_database(client, texts):
    """GET text endpoint should return a text entry from database"""
    res = client.get('/api/texts')

    assert res.status == '200 OK'
    assert isinstance(res.json, list)
    assert len(res.json) == 1
    assert res.json[0]['text_string'] == 'Example text 1'
    assert isinstance(res.json[0]['id'], str)
    assert isinstance(res.json[0]['created_at'], str)
    assert isinstance(res.json[0]['updated_at'], str)

@pytest.mark.parametrize('texts', [2], indirect=True)
def test_get_returns_multiple_texts_from_database(client, texts):
    """GET text endpoint should multiple text entries from database"""
    res = client.get('/api/texts')

    assert isinstance(res.json, list)
    assert len(res.json) == 2
    assert res.json[0]['text_string'] == 'Example text 2'
    assert res.json[1]['text_string'] == 'Example text 1'

@pytest.mark.parametrize('texts', [11], indirect=True)
def test_get_returns_10_texts_from_database(client, texts):
    """GET text endpoint should return the last 10 texts in reverse chronological order"""
    res = client.get('/api/texts')

    assert isinstance(res.json, list)
    assert len(res.json) == 10
    assert res.json[0]['text_string'] == 'Example text 11'
    assert res.json[9]['text_string'] == 'Example text 2'

