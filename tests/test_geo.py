import json
import pytest
from setup import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Destination' in response.data

def test_location_not_found(client):
    response = client.get('/?destination=129w92')

    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert data['status'] == 0
    

def test_distance_not_found(client):
    response = client.get('/?destination=jakarta')

    data = json.loads(response.get_data(as_text=True))
    assert response.status_code == 404
    assert data['status'] == 2

def test_route_not_found(client):
    response = client.get('/random')

    assert response.status_code == 404
    assert b'NOT FOUND' in response.data

def test_inside_origin(client):
    response = client.get('/?destination=moscow')

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data['status'] == 3

def test_destination_empty(client):
    response = client.get('/?destination=')

    assert response.status_code == 302

    