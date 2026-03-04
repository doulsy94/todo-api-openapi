import connexion
from flask import jsonify
from openapi_server.models.task import Task
from openapi_server.models.task_input import TaskInput

# Base de données en mémoire (simple liste)
tasks_db = []
task_id_counter = 1

def get_tasks():
    """Retourne toutes les tâches"""
    return [task.to_dict() for task in tasks_db]

def create_task():
    """Crée une nouvelle tâche"""
    global task_id_counter
    if connexion.request.is_json:
        # Convertir la requête JSON en objet TaskInput
        task_input = TaskInput.from_dict(connexion.request.get_json())
        # Créer une nouvelle tâche avec un ID unique
        new_task = Task(
            id=task_id_counter,
            title=task_input.title,
            completed=task_input.completed if task_input.completed is not None else False
        )
        tasks_db.append(new_task)
        task_id_counter += 1
        return jsonify(new_task.to_dict()), 201
    return jsonify({"error": "Request must be JSON"}), 400

def get_task_by_id(task_id):
    """Récupère une tâche par son ID"""
    for task in tasks_db:
        if task.id == task_id:
            return jsonify(task.to_dict()), 200
    return jsonify({"code": 404, "message": "Task not found"}), 404