from uuid import uuid4

from fastapi import status


def test_register_user_success(client):
    payload = {'email': f'user-{uuid4().hex[:8]}@example.com', 'password': 'Password123'}

    response = client.post('/login/register', json=payload)

    assert response.status_code == status.HTTP_201_CREATED


def test_login_user_success(client):
    email = f'user-{uuid4().hex[:8]}@example.com'
    password = 'Password123'

    client.post('/login/register', json={'email': email, 'password': password})
    response = client.post('/login', json={'email': email, 'password': password})

    assert response.status_code == status.HTTP_200_OK
    assert 'email' in response.json()


def test_register_existing_user_returns_400(client):
    email = f'user-{uuid4().hex[:8]}@example.com'
    payload = {'email': email, 'password': 'Password123'}

    client.post('/login/register', json=payload)
    response = client.post('/login/register', json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
