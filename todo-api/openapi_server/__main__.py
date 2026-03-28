#!/usr/bin/env python3

import connexion
import logging
import sys
from prometheus_flask_exporter import PrometheusMetrics
from pythonjsonlogger import jsonlogger
from openapi_server import encoder
from openapi_server.metrics import update_metrics
from openapi_server.task_storage import tasks_db
from openapi_server.controllers import default_controller

# --- OpenTelemetry imports ---
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# --- Configuration du logging (comme avant) ---
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s %(module)s %(lineno)d'
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

setup_logging()

# --- Configuration OpenTelemetry ---
def setup_tracing():
    resource = Resource(attributes={
        SERVICE_NAME: "todo-api"
    })
    provider = TracerProvider(resource=resource)
    # Envoi des traces à Tempo via OTLP (gRPC) sur le port 4317
    exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Instrumenter Flask et Requests
    FlaskInstrumentor().instrument()
    RequestsInstrumentor().instrument()

setup_tracing()

#
class CustomResolver(connexion.resolver.Resolver):
    def __init__(self, function_map):
        super().__init__()
        self.function_map = function_map

    def resolve_function_from_operation_id(self, operation_id):
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