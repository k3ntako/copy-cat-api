from flask import json

from src.copycat import create_app

def test_health_check():
    with create_app().test_client() as client:
        res = client.get('/health', follow_redirects=True)
        data = json.loads(res.data)
        
    assert data['status'] == 'UP'
