# API управления задачами (To-Do) – Полные лабораторные работы

Этот репозиторий содержит исходный код REST API для управления списком задач, разработанный в рамках нескольких лабораторных работ:

1. **API First с OpenAPI** – проектирование, генерация и реализация API на основе спецификации OpenAPI 3.0.
2. **Мониторинг метрик** – добавление HTTP-метрик и продуктовых метрик (общее количество задач, выполненных, просроченных) с помощью Prometheus и визуализация в Grafana.
3. **Мониторинг логов** – экспорт структурированных логов в формате JSON, сбор через Loki и визуализация в Grafana.

## Описание работ

### 1. API First
- Составление файла спецификации `openapi.yaml`, описывающего API.
- Генерация каркаса сервера на Python/Flask с помощью OpenAPI Generator.
- Реализация бизнес-логики (CRUD в памяти, срока выполнения задач).
- Интерактивная документация Swagger UI.

### 2. Метрики
- Инструментирование приложения библиотекой `prometheus_flask_exporter`.
- Пользовательские метрики:
  - `tasks_total` – общее количество задач
  - `tasks_completed` – количество выполненных задач
  - `tasks_overdue` – количество просроченных задач (срок выполнения истёк, задача не выполнена)
- Настройка Prometheus для сбора метрик с эндпоинта `/metrics`.
- Создание дашборда в Grafana с метриками HTTP и продуктовыми метриками.

### 3. Логи
- Добавление структурированных логов в формате JSON с помощью `python-json-logger`.
- Запись логов в файл `app.log`.
- Установка и настройка **Loki** (агрегатор логов) и **Promtail** (сборщик логов).
- Подключение Loki как источника данных в Grafana.
- Создание дашборда для визуализации логов с возможностью поиска (например, `{job="todo-api"}`, фильтрация по уровню и т.д.).

## Используемые технологии

- **OpenAPI 3.0.0** – спецификация
- **OpenAPI Generator** (v7.20.0) – генерация кода
- **Python 3.8+** – язык
- **Flask / Connexion** – веб-фреймворк
- **Swagger UI** – интерактивная документация
- **Prometheus** – сбор метрик
- **Grafana** – визуализация метрик и логов
- **Loki** – агрегация логов
- **Promtail** – сбор логов
- **prometheus_flask_exporter** – экспорт метрик из Flask
- **python-json-logger** – логи в JSON

## Установка и запуск

### Предварительные требования
- Python 3.8 или выше
- Git (опционально)
- [Prometheus](https://prometheus.io/download/) (скачать и распаковать)
- [Grafana](https://grafana.com/grafana/download) (скачать и установить)
- [Loki и Promtail](https://github.com/grafana/loki/releases) (скачать архивы `loki-windows-amd64.exe.zip` и `promtail-windows-amd64.exe.zip`)

### Шаги

#### 1. Клонировать репозиторий
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

6.**Настроить Grafana**
  -Запустите Grafana (например, grafana-server.exe).
  -Откройте http://localhost:3000 (логин admin/admin).
  -Добавьте источник данных Prometheus (URL http://localhost:9090).
  -Добавьте источник данных Loki (URL http://localhost:3100).

7.**Импортировать дашборды (или создать вручную)**
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
