import os
import contextlib

import pytest

from src.copycat import create_app
from src.copycat.database import db
from src.copycat.database.models.text import Text

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    os.environ["APP_CONFIG"] = "config.TestingConfig"
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

# Commits to database mock text rows
# The number of rows can be passed in using @pytest.mark.parametrize
@pytest.fixture
def texts(app, request):
    """Mock text entries in database."""
    with app.app_context():
        for i in range(1, request.param + 1):
            text = Text(f"Example text {i}")
            db.session.add(text)

        db.session.commit()

    return text