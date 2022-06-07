import json
from project.app import app, init_db, db
from pathlib import Path
import pytest
import os

TEST_DB = 'flasker.db'

@pytest.fixture
def client():
    BASE_DIR = Path(__file__).parent.parent
    app.config['DATABASE'] = BASE_DIR.joinpath(TEST_DB)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR.joinpath(TEST_DB)}'

    # init_db() # setup
    db.create_all()
    yield app.test_client()
    # init_db()  # tear down
    db.drop_all()

def login(client, username, password):
    """Helper function to login"""
    return client.post('/login', data=dict(username=username, password=password), follow_redirects=True)

def logout(client):
    """Helper function to logout"""
    return client.get('/logout', follow_redirects=True)

def test_index(client):
    login(client, app.config["USERNAME"], app.config["PASSWORD"])
    response = client.get('/', content_type='html/text')
    assert response.status_code == 200

def test_database(client):
    tester = Path(TEST_DB).is_file()
    assert tester

def test_empty_db(client):
    login(client, app.config["USERNAME"], app.config["PASSWORD"])
    rv = client.get('/')
    assert b"No entries yet. Add some!" in rv.data

def test_login_logout(client):
    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"])
    assert b"You were logged in" in rv.data
    rv = logout(client)
    assert b"You were logged out" in rv.data
    rv = login(client, app.config["USERNAME"] + "x", app.config["PASSWORD"])
    assert b"Invalid username" in rv.data
    rv = login(client, app.config["USERNAME"], app.config["PASSWORD"] + "x")
    assert b"Invalid password" in rv.data

def test_messages(client):
    """Ensure that user can post messages"""
    login(client, app.config["USERNAME"], app.config["PASSWORD"])
    rv = client.post( "/add", data=dict(title="<Hello>", text="<strong>HTML</strong> allowed here"), follow_redirects=True, )
    assert b"No entries here so far" not in rv.data
    assert b"&lt;Hello&gt;" in rv.data
    assert b"<strong>HTML</strong> allowed here" in rv.data

def test_delete_message(client):
    """ensure the messages are deleted"""
    # rv = client.get("/delete/1")
    # data = json.loads(rv.data)
    # assert data["status"] == 0
    login(client, app.config["USERNAME"], app.config["PASSWORD"])
    rv = client.get("/delete/1")
    data = json.loads(rv.data)
    assert data["status"] == 1