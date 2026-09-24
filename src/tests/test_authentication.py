from uuid import uuid4

from fastapi import status


def test_create_token_success(client):
    email = f'user-{uuid4().hex[:8]}@example.com'
    password = 'Password123'

    client.post('/login/register', json={'email': email, 'password': password})
    response = client.post('/token', json={'email': email, 'password': password})

    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.json()


def test_token_authentication_returns_user(client):
    email = f'user-{uuid4().hex[:8]}@example.com'
    password = 'Password123'

    client.post('/login/register', json={'email': email, 'password': password})
    token_response = client.post('/token', json={'email': email, 'password': password})
    token = token_response.json()['access_token']

    auth_header = {'Authorization': f'Bearer {token}'}
    protected_response = client.get('/task/list', headers=auth_header)

    assert protected_response.status_code == status.HTTP_200_OK
