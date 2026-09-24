from uuid import uuid4

from fastapi import status


def build_headers(client, email=None, password='Password123'):
    email = email or f'user-{uuid4().hex[:8]}@example.com'

    register_response = client.post('/login/register', json={'email': email, 'password': password})
    assert register_response.status_code == status.HTTP_201_CREATED

    token_response = client.post('/token', json={'email': email, 'password': password})
    assert token_response.status_code == status.HTTP_201_CREATED

    return {'Authorization': f"Bearer {token_response.json()['access_token']}"}


def test_create_task_success(client):
    headers = build_headers(client)
    payload = {'task_name': 'Estudar pytest', 'init_time': '08:00:00', 'end_time': '09:00:00'}

    response = client.post('/task/', json=payload, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    tasks = client.get('/task/list', headers=headers).json()
    assert any(task['task_name'] == 'Estudar pytest' for task in tasks)


def test_list_tasks_returns_only_current_user_tasks(client):
    first_headers = build_headers(client, email=f'first-{uuid4().hex[:8]}@example.com')
    second_headers = build_headers(client, email=f'second-{uuid4().hex[:8]}@example.com')

    client.post('/task/', json={'task_name': 'Tarefa do primeiro'}, headers=first_headers)
    client.post('/task/', json={'task_name': 'Tarefa do segundo'}, headers=second_headers)

    first_tasks = client.get('/task/list', headers=first_headers).json()
    second_tasks = client.get('/task/list', headers=second_headers).json()

    assert [task['task_name'] for task in first_tasks] == ['Tarefa do primeiro']
    assert [task['task_name'] for task in second_tasks] == ['Tarefa do segundo']


def test_list_tasks_requires_authentication(client):
    response = client.get('/task/list')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_task_success(client):
    headers = build_headers(client)
    create_response = client.post('/task/', json={'task_name': 'Excluir depois'}, headers=headers)
    assert create_response.status_code == status.HTTP_200_OK

    task_id = client.get('/task/list', headers=headers).json()[0]['id']
    response = client.delete(f'/task/{task_id}', headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'Status': 'Task Deleted'}
    assert client.get('/task/list', headers=headers).json() == []
