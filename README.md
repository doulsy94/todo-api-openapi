# API управления задачами (To-Do) – лабораторные работы API First и мониторинг

Этот репозиторий содержит исходный код REST API для управления списком задач (To-Do list), выполненной в рамках двух лабораторных работ:

1. **API First с OpenAPI** – проектирование, генерация и реализация API на основе спецификации OpenAPI 3.0.
2. **Мониторинг** – добавление метрик, их сбор с помощью Prometheus и визуализация в Grafana.

## Описание работы

### Часть 1: API First
Целью первой части была реализация API в соответствии с методологией **API First** (design-first). Основные этапы:

- **Разработка контракта**: создание файла `openapi.yaml`, описывающего ресурсы, методы, параметры и модели данных.
- **Генерация скелета сервера**: использование инструмента **OpenAPI Generator** для автоматической генерации структуры сервера на Python с использованием Flask (генератор `python-flask`).
- **Реализация бизнес-логики**: добавление кода для управления списком задач в памяти (создание, просмотр, поиск по ID).
- **Интерактивное тестирование**: автоматически сгенерированная документация с помощью **Swagger UI**, позволяющая тестировать API непосредственно из браузера.

Данный проект демонстрирует, как правильно определённая спецификация может служить единым контрактом между клиентом и сервером, упрощая разработку, документирование и сопровождение.

### Часть 2: Мониторинг
Вторая часть посвящена добавлению observability в проект:

- **Инструментирование Flask-приложения** с помощью библиотеки `prometheus_flask_exporter` для сбора стандартных HTTP-метрик (количество запросов, время ответа, коды ответов).
- **Настройка Prometheus** для сбора метрик с эндпоинта `/metrics`.
- **Подключение Grafana** для визуализации собранных данных и создания дашборда.

Теперь можно наблюдать за работой API в реальном времени: видеть нагрузку, время ответа и другие полезные метрики.

## Используемые технологии

- [OpenAPI 3.0.0](https://swagger.io/specification/) – спецификация API
- [OpenAPI Generator](https://openapi-generator.tech/) (v7.20.0) – генерация кода
- Python 3.8+ – язык реализации
- [Flask](https://flask.palletsprojects.com/) / [Connexion](https://github.com/zalando/connexion) – веб-фреймворк
- [Swagger UI](https://swagger.io/tools/swagger-ui/) – интерактивная документация
- [Prometheus](https://prometheus.io/) – сбор и хранение метрик
- [Grafana](https://grafana.com/) – визуализация метрик
- [prometheus_flask_exporter](https://github.com/rycus86/prometheus_flask_exporter) – экспорт метрик из Flask
- Git – система контроля версий

## Установка и запуск

### Предварительные требования

- Установленный Python 3.8 или выше
- `pip` (менеджер пакетов Python)
- Git (опционально, для клонирования)
- [Prometheus](https://prometheus.io/download/) (скачайте и распакуйте архив)
- [Grafana](https://grafana.com/grafana/download) (скачайте и установите)

### Шаги

1. **Клонировать репозиторий**

   ```bash
   git clone https://github.com/doulsy94/todo-api-openapi.git
   cd todo-api-openapi
   ```

2. **Установить зависимости Python**

```bash
pip install -r requirements.txt
```

3. **Запустить сервер**

```bash
python -m openapi_server
```

- Сервер запустится по адресу http://localhost:8080.
- Документация Swagger UI доступна на http://localhost:8080/ui/.
- Метрики для Prometheus доступны на http://localhost:8080/metrics.

## Настройка мониторинга

**Prometheus**

1. Создайте файл конфигурации prometheus.yml (пример приведён ниже) или используйте готовый из репозитория.

2. Запустите Prometheus, указав путь к конфигурации:

```bash
prometheus.exe --config.file="C:\путь\к\prometheus.yml"
Пример содержимого prometheus.yml:

yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "todo-api"
    static_configs:
      - targets: ["localhost:8080"]
    metrics_path: "/metrics"
```

3. Проверьте, что цель todo-api появилась в статусе UP в веб-интерфейсе Prometheus по адресу http://localhost:9090/targets.

**Grafana**

1. Запустите Grafana (по умолчанию доступна на http://localhost:3000, логин/пароль: admin/admin).

2. Добавьте Prometheus как источник данных:

   - Configuration → Data Sources → Add data source → Prometheus.

   - В поле URL укажите http://localhost:9090.

   - Нажмите Save & Test.

3. Создайте новый дашборд:

   - Создайте новый dashboard (кнопка "+" в боковом меню → Dashboard).

   - Добавьте новый panel.

   - В качестве источника данных выберите Prometheus.

   - Введите PromQL-запрос, например:

```bash
rate(flask_http_request_total[1m])
```

Настройте отображение и сохраните дашборд.