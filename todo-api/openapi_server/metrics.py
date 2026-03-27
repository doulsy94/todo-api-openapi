from prometheus_client import Gauge
from .task_storage import tasks_db
from datetime import date

# Define custom metrics
tasks_total = Gauge('tasks_total', 'Total number of tasks')
tasks_completed = Gauge('tasks_completed', 'Number of completed tasks')
tasks_overdue = Gauge('tasks_overdue', 'Number of overdue tasks (due date in past and not completed)')

def update_metrics():
    """Recalculate and set all task-related metrics."""
    total = len(tasks_db)
    completed = sum(1 for t in tasks_db if t.completed)
    today = date.today()
    overdue = sum(1 for t in tasks_db if t.due_date is not None and t.due_date < today and not t.completed)
    tasks_total.set(total)
    tasks_completed.set(completed)
    tasks_overdue.set(overdue)