#!/usr/bin/env python3

import connexion
from connexion.resolver import Resolver
from prometheus_flask_exporter import PrometheusMetrics
from openapi_server import encoder
from openapi_server.metrics import update_metrics
from openapi_server.task_storage import tasks_db
from openapi_server.controllers import default_controller

class CustomResolver(Resolver):
    def __init__(self, function_map):
        super().__init__()
        self.function_map = function_map

    def resolve_function_from_operation_id(self, operation_id):
        # Retourne la fonction correspondante depuis le dictionnaire
        return self.function_map.get(operation_id)

def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder

    function_map = {
        'get_tasks': default_controller.get_tasks,
        'create_task': default_controller.create_task,
        'get_task_by_id': default_controller.get_task_by_id,
        'update_task': default_controller.update_task,
    }

    resolver = CustomResolver(function_map)

    app.add_api(
        'openapi.yaml',
        arguments={'title': 'To-Do List API'},
        pythonic_params=True,
        resolver=resolver
    )

    flask_app = app.app
    metrics = PrometheusMetrics(flask_app)
    metrics.info('app_info', 'Todo API', version='1.0.0')

    update_metrics()

    app.run(port=8080)

if __name__ == '__main__':
    main()