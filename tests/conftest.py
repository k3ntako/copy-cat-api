import contextlib

import pytest
from sqlalchemy.schema import MetaData
from sqlalchemy import create_engine

from src.copycat import create_app
from src.copycat.database import db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()

    yield app

    with app.app_context():
        with contextlib.closing(db.engine.connect()) as con:
            transaction = con.begin()
            con.execute("TRUNCATE texts;")
            transaction.commit()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()