import connexion
import logging
from flask import jsonify
from openapi_server.models.task import Task
from openapi_server.models.task_input import TaskInput
from openapi_server.task_storage import tasks_db, task_id_counter
from openapi_server.metrics import update_metrics

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

# Obtenir un logger pour ce module
logger = logging.getLogger(__name__)
# Obtenir un traceur pour créer des spans personnalisées
tracer = trace.get_tracer(__name__)

def get_tasks():
    """Return all tasks."""
    logger.info("GET /tasks called")
    with tracer.start_as_current_span("get_tasks") as span:
        span.set_attribute("num_tasks", len(tasks_db))
        return [task.to_dict() for task in tasks_db]

def create_task():
    """Create a new task."""
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

    with tracer.start_as_current_span("create_task") as span:
        # Ajouter des attributs à la span pour enrichir la trace
        span.set_attribute("task.id", new_task.id)
        span.set_attribute("task.title", new_task.title)
        span.set_attribute("task.completed", new_task.completed)
        if new_task.due_date:
            span.set_attribute("task.due_date", new_task.due_date.isoformat())

        tasks_db.append(new_task)
        task_id_counter += 1
        update_metrics()
        logger.info(
            "Task created",
            extra={'task_id': new_task.id, 'title': new_task.title}
        )
        return jsonify(new_task.to_dict()), 201

def get_task_by_id(task_id):
    """Get a task by ID."""
    with tracer.start_as_current_span("get_task_by_id") as span:
        span.set_attribute("task.id", task_id)
        for task in tasks_db:
            if task.id == task_id:
                logger.info(f"Task retrieved", extra={'task_id': task_id})
                return jsonify(task.to_dict()), 200
        logger.warning(f"Task not found", extra={'task_id': task_id})
        span.set_status(Status(StatusCode.ERROR, "Task not found"))
        return jsonify({"code": 404, "message": "Task not found"}), 404

def update_task(task_id):
    """Update a task (partial update)."""
    if not connexion.request.is_json:
        logger.warning(f"PATCH /tasks/{task_id} called with non-JSON")
        return jsonify({"error": "Request must be JSON"}), 400

    task_input = TaskInput.from_dict(connexion.request.get_json())

    with tracer.start_as_current_span("update_task") as span:
        span.set_attribute("task.id", task_id)
        span.set_attribute("task.title_updated", task_input.title is not None)
        span.set_attribute("task.completed_updated", task_input.completed is not None)
        span.set_attribute("task.due_date_updated", task_input.due_date is not None)

        for task in tasks_db:
            if task.id == task_id:
                if task_input.title is not None:
                    task.title = task_input.title
                if task_input.completed is not None:
                    task.completed = task_input.completed
                if task_input.due_date is not None:
                    task.due_date = task_input.due_date
                update_metrics()
                logger.info(
                    f"Task updated",
                    extra={'task_id': task_id, 'changes': task_input.to_dict()}
                )
                return jsonify(task.to_dict()), 200

        logger.warning(f"Task not found for update", extra={'task_id': task_id})
        span.set_status(Status(StatusCode.ERROR, "Task not found"))
        return jsonify({"code": 404, "message": "Task not found"}), 404