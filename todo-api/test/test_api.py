import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from openapi_server import task_storage
from openapi_server.controllers import default_controller
import connexion
from connexion.resolver import Resolver

class CustomResolver(Resolver):
    def __init__(self, function_map):
        super().__init__()
        self.function_map = function_map

    def resolve_function_from_operation_id(self, operation_id):
        return self.function_map.get(operation_id)

@pytest.fixture
def client():
    task_storage.tasks_db.clear()
    task_storage.task_id_counter = 1

    spec_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'openapi_server', 'openapi')
    app = connexion.App(__name__, specification_dir=spec_dir)

    function_map = {
        'get_tasks': default_controller.get_tasks,
        'create_task': default_controller.create_task,
        'get_task_by_id': default_controller.get_task_by_id,
        'update_task': default_controller.update_task,
    }
    resolver = CustomResolver(function_map)

    # Important : ajouter pythonic_params=True pour convertir camelCase en snake_case
    app.add_api('openapi.yaml', resolver=resolver, pythonic_params=True)
    with app.app.test_client() as test_client:
        yield test_client

def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.json == []

def test_create_task(client):
    data = {"title": "Test task", "completed": False, "due_date": "2026-12-31"}
    response = client.post('/tasks', json=data)
    assert response.status_code == 201
    assert response.json['title'] == "Test task"

def test_get_task_by_id(client):
    post_resp = client.post('/tasks', json={"title": "Get me", "completed": False})
    task_id = post_resp.json['id']
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json['title'] == "Get me"

def test_update_task(client):
    post_resp = client.post('/tasks', json={"title": "To update", "completed": False})
    task_id = post_resp.json['id']
    # Inclure le titre pour éviter l'erreur de validation (car title est requis)
    response = client.patch(f'/tasks/{task_id}', json={"title": "To update", "completed": True})
    assert response.status_code == 200
    assert response.json['completed'] == True

def test_get_task_not_found(client):
    response = client.get('/tasks/9999')
    assert response.status_code == 404