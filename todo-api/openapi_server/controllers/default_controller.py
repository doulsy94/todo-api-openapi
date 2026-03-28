import connexion
import logging
from flask import jsonify
from openapi_server.models.task import Task
from openapi_server.models.task_input import TaskInput
from openapi_server.task_storage import tasks_db, task_id_counter
from openapi_server.metrics import update_metrics

logger = logging.getLogger(__name__)

def get_tasks():
    logger.info("GET /tasks called")
    return [task.to_dict() for task in tasks_db]

def create_task():
    global task_id_counter
    if not connexion.request.is_json:
        logger.warning("POST /tasks called with non-JSON request")
        return jsonify({"error": "Request must be JSON"}), 400

    task_input = TaskInput.from_dict(connexion.request.get_json())
    new_task = Task(
        id=task_id_counter,
        title=task_input.title,
        completed=task_input.completed if task_input.completed is not None else False,
        due_date=task_input.due_date
    )
    tasks_db.append(new_task)
    task_id_counter += 1
    update_metrics()
    logger.info(f"Task created", extra={'task_id': new_task.id, 'title': new_task.title})
    return jsonify(new_task.to_dict()), 201

def get_task_by_id(task_id):
    for task in tasks_db:
        if task.id == task_id:
            logger.info(f"Task retrieved", extra={'task_id': task_id})
            return jsonify(task.to_dict()), 200
    logger.warning(f"Task not found", extra={'task_id': task_id})
    return jsonify({"code": 404, "message": "Task not found"}), 404

def update_task(task_id):
    if not connexion.request.is_json:
        logger.warning(f"PATCH /tasks/{task_id} called with non-JSON")
        return jsonify({"error": "Request must be JSON"}), 400

    task_input = TaskInput.from_dict(connexion.request.get_json())
    for task in tasks_db:
        if task.id == task_id:
            if task_input.title is not None:
                task.title = task_input.title
            if task_input.completed is not None:
                task.completed = task_input.completed
            if task_input.due_date is not None:
                task.due_date = task_input.due_date
            update_metrics()
            logger.info(f"Task updated", extra={'task_id': task_id, 'changes': task_input.to_dict()})
            return jsonify(task.to_dict()), 200
    logger.warning(f"Task not found for update", extra={'task_id': task_id})
    return jsonify({"code": 404, "message": "Task not found"}), 404