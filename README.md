# API управления задачами (To-Do) – Полные лабораторные работы

Этот репозиторий содержит исходный код REST API для управления списком задач, разработанный в рамках пяти лабораторных работ, направленных на создание полноценной наблюдаемой системы (observability):

1. **API First с OpenAPI** – проектирование, генерация и реализация API на основе спецификации OpenAPI 3.0.
2. **Метрики Prometheus** – сбор стандартных HTTP-метрик (количество запросов, время ответа, коды ответов).
3. **Продуктовые метрики** – пользовательские метрики: `tasks_total`, `tasks_completed`, `tasks_overdue`.
4. **Логи** – структурированные JSON-логи, сбор через Loki и визуализация в Grafana.
5. **Трассировка (Tracing)** – распределённая трассировка с помощью OpenTelemetry и Grafana Tempo.

Все компоненты централизованно отображаются в **Grafana**, что позволяет анализировать поведение сервиса в реальном времени.

---

## Описание работ

### 1. API First (OpenAPI)

- Создание файла спецификации `openapi.yaml`, описывающего ресурсы, методы и модели данных.
- Генерация серверного кода (Python/Flask) с помощью **OpenAPI Generator**.
- Реализация бизнес-логики CRUD в памяти:
  - Создание задачи (POST /tasks)
  - Получение всех задач (GET /tasks)
  - Получение задачи по ID (GET /tasks/{taskId})
  - Обновление задачи (PATCH /tasks/{taskId}) – поддержка `due_date` (срок выполнения) и статуса `completed`.
- Интерактивная документация **Swagger UI**.

### 2. Метрики (Prometheus)

- Инструментирование Flask-приложения через `prometheus_flask_exporter`.
- Автоматический сбор стандартных HTTP-метрик:
  - `flask_http_request_total` – количество запросов
  - `flask_http_request_duration_seconds` – длительность запросов
- Экспорт метрик на эндпоинте `/metrics`.

### 3. Продуктовые метрики

- Пользовательские метрики, обновляемые при изменении данных:
  - `tasks_total` – общее количество задач
  - `tasks_completed` – количество выполненных задач
  - `tasks_overdue` – количество просроченных задач (срок выполнения в прошлом, задача не выполнена)
- Метрики доступны на `/metrics` и собираются Prometheus.

### 4. Логи (Loki)

- Структурированные логи в формате JSON с помощью `python-json-logger`.
- Логи записываются в файл `app.log` и в консоль.
- **Promtail** читает файл и отправляет логи в **Loki**.
- В Grafana добавлен источник данных Loki, создан дашборд с панелью для просмотра логов с возможностью фильтрации.

### 5. Трассировка (Tempo)

- Инструментирование Flask через `opentelemetry-instrumentation-flask`.
- Создание пользовательских спанов в контроллерах (`create_task`, `update_task`, `get_task_by_id`) с добавлением атрибутов (например, `task.id`, `task.title`).
- Экспорт трасс по протоколу OTLP (gRPC) в **Grafana Tempo**.
- В Grafana добавлен источник данных Tempo, организован поиск трасс по сервису `todo-api` и просмотр детальных диаграмм.

---

## Используемые технологии

- **OpenAPI 3.0.0** – спецификация API
- **OpenAPI Generator** (v7.20.0) – генерация кода
- **Python 3.8+** – язык реализации
- **Flask** / **Connexion** – веб-фреймворк
- **Swagger UI** – интерактивная документация
- **Prometheus** – сбор и хранение метрик
- **Grafana** – визуализация метрик, логов и трасс
- **Loki** – агрегация логов
- **Promtail** – сбор логов
- **Tempo** – хранение и поиск трасс
- **OpenTelemetry** – инструментирование кода
- **prometheus_flask_exporter** – экспорт метрик из Flask
- **python-json-logger** – логи в формате JSON
- **Git** – система контроля версий

---

## Установка и запуск

### Предварительные требования

- Python 3.8 или выше, `pip`
- Git (опционально)
- [Prometheus](https://prometheus.io/download/) (скачать и распаковать)
- [Grafana](https://grafana.com/grafana/download) (скачать и установить)
- [Loki и Promtail](https://github.com/grafana/loki/releases) (скачать `loki-windows-amd64.exe.zip` и `promtail-windows-amd64.exe.zip`)
- [Tempo](https://github.com/grafana/tempo/releases) (скачать `tempo_<version>_windows_amd64.zip`)

### Шаги

1. **Клонировать репозиторий**

   ```bash
   git clone https://github.com/doulsy94/todo-api-openapi.git
   cd todo-api-openapi
   ```

2.**Установить зависимости Python**

  ```bash
  pip install -r requirements.txt
  ```

3.**Запустить API**

 ```bash
  cd todo-api
  python -m openapi_server
 ```

  API будет доступно по адресу http://localhost:8080.
  Swagger UI: http://localhost:8080/ui/
  Метрики Prometheus: http://localhost:8080/metrics

4.**Запустить Prometheus**

 -Поместите файл конфигурации prometheus.yml в папку Prometheus (или используйте приложенный).

 -Запустите Prometheus:

  ```bash
  .(.venv) PS C:\prometheus> .\prometheus.exe --config.file="C:\Users\Doul Sy\Desktop\labo-openapi-todo\prometheus.yml"
  ```

Пример prometheus.yml:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "todo-api"
    static_configs:
      - targets: ["localhost:8080"]
    metrics_path: "/metrics"
```

-Проверьте, что цель todo-api появилась в статусе UP в веб-интерфейсе Prometheus по адресу http://localhost:9090/targets


5.**Запустить Loki и Promtail**
 -Распакуйте loki-windows-amd64.exe и promtail-windows-amd64.exe в папку (например, C:\loki).

 -Создайте файлы конфигурации (примеры ниже).

 -Запустите Loki:

 ```bash
 (.venv) PS C:\loki> .\promtail-windows-amd64.exe --config.file=promtail-local-config.yaml 
 ```

 -Запустите Promtail:

 ```bash
 (.venv) PS C:\loki> .\promtail-windows-amd64.exe --config.file=promtail-local-config.yaml
 ```

Пример loki-local-config.yaml:

```yaml
auth_enabled: false
server:
  http_listen_port: 3100
common:
  path_prefix: C:/loki/data
  storage:
    filesystem:
      chunks_directory: C:/loki/data/chunks
      rules_directory: C:/loki/data/rules
  replication_factor: 1
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory
schema_config:
  configs:
    - from: 2020-05-15
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h
limits_config:
  allow_structured_metadata: true
  volume_enabled: true
```

Пример promtail-local-config.yaml (укажите абсолютный путь к app.log):

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0
positions:
  filename: C:/loki/positions.yaml
clients:
  - url: http://localhost:3100/loki/api/v1/push
scrape_configs:
  - job_name: todo-api
    static_configs:
      - targets:
          - localhost
        labels:
          job: todo-api
          __path__: "C:/Users/Doul Sy/Desktop/labo-openapi-todo/todo-api/app.log"
```

6.**Запустить Tempo**

- Распаковать tempo.exe в папку (например, C:\tempo).
- Создать tempo-local-config.yaml (пример – в репозитории).
- Запустить: .\tempo.exe --config.file=tempo-local-config.yaml 

Пример loki-local-config.yaml:

```yaml
server:
  http_listen_port: 3200
  grpc_listen_port: 9096
distributor:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: "0.0.0.0:4317"
ingester:
  trace_idle_period: 10s
  max_block_bytes: 1_000_000
  max_block_duration: 5m
compactor:
  compaction:
    block_retention: 24h
storage:
  trace:
    backend: local
    local:
      path: C:/tempo/data
    wal:
      path: C:/tempo/wal
memberlist:
  abort_if_cluster_join_fails: false
```

7.**Настроить Grafana**
  -Запустите Grafana (например, grafana-server.exe).
  -Откройте http://localhost:3000 (логин admin/admin).
  -Добавьте источник данных Prometheus (URL http://localhost:9090).
  -Добавьте источник данных Loki (URL http://localhost:3100).
  -Добавьте источник данных Tempo (URL http://localhost:3200).

8.**Импортировать дашборды (или создать вручную)**
Вы можете импортировать JSON-дашборд (если он есть в репозитории) или создать панели вручную.

Примеры запросов для метрик:

  -tasks_total – общее количество задач

  -tasks_completed – выполненные задачи

  -tasks_overdue – просроченные задачи

  -(tasks_completed / tasks_total) * 100 – процент выполнения

Запросы Loki:

  -{job="todo-api"} – все логи приложения

  -{job="todo-api"} |= "ERROR" – только ошибки

  -{job="todo-api"} | json | task_id="1" – логи по конкретной задаче

Запросы Tempo:

 -{ .service.name = "todo-api" }