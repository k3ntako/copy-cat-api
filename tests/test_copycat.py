from flask import json

from copycat import create_app

def test_health_check():
    with create_app().test_client() as client:
        res = client.get('/health')
        data = json.loads(res.data)
        
    assert data['status'] == 'UP'