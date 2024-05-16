from flask import Flask, app
import pytest

from core.libs.exceptions import FyleError


def test_root_route(client):
    """
    Test the root route
    """
    response = client.get('/')
    data = response.json
    assert response.status_code == 200
    assert 'status' in data
    assert data['status'] == 'ready'
    assert 'time' in data 



def test_blueprint_registrations(client):
    """
    Test if the required blueprints are registered correctly
    """
    # Check student assignments resources
    response = client.get('/student/assignments')
    assert response.status_code == 401  # Expect 401 Unauthorized without authentication

    # Check teacher assignments resources
    response = client.get('/teacher/assignments')
    assert response.status_code == 401  # Expect 401 Unauthorized without authentication

    # Check principal resources
    response = client.get('/principal/assignments')
    assert response.status_code == 401  # Expect 401 Unauthorized without authentication
