# Report (placeholder)

> ⚠️ **Work in progress.** This report will be completed later.

## Цель проекта

Минимальный LangChain-агент — обёртка над API на естественном языке.

## Архитектура

TODO: описать компоненты (CLI, agent, tools, mock API).

## API (mock)

**Выбранный домен:** минимальный helpdesk / система управления заявками
(task management).

**Поддерживаемые операции:**

- `POST /tasks` — создание заявки (`title`, `priority`, `description`),
  статус по умолчанию `new`.
- `GET /tasks/{task_id}` — получение заявки по id (404, если не найдена).
- `PATCH /tasks/{task_id}/status` — смена статуса
  (`new`, `in_progress`, `resolved`, `closed`; 400 при недопустимом статусе,
  404 при отсутствии заявки).
- `GET /tasks` — список заявок с опциональной фильтрацией по `status`
  и `priority`.
- `GET /stats` — статистика (`total`, `by_status`, `by_priority`).
- `GET /` — имя API и список эндпоинтов.
- `GET /health` — проверка работоспособности.

API является **локальным** и хранит данные **в памяти** (in-memory),
база данных не используется.

## LangChain-инструменты (tools)

Агент вызывает mock Task API через LangChain-инструменты, объявленные с
помощью декоратора `@tool` в `app/tools/task_api_tool.py`. Каждый инструмент
выполняет **реальный HTTP-запрос** через `requests`, печатает отладочную
строку `[TOOL CALL] ...` перед запросом и возвращает JSON-строку.

| Инструмент | HTTP-метод API |
|------------|----------------|
| `create_task` | `POST /tasks` |
| `get_task` | `GET /tasks/{task_id}` |
| `update_task_status` | `PATCH /tasks/{task_id}/status` |
| `list_tasks` | `GET /tasks` |
| `get_task_stats` | `GET /stats` |

Базовый URL читается из переменной окружения `TASK_API_BASE_URL`
(по умолчанию `http://localhost:8000`), `.env` загружается через
`python-dotenv`.

### Ссылки на строки кода

(Актуально на момент реализации; обновлять при изменении файла.)

- `app/tools/task_api_tool.py:61-81` — объявление инструмента `create_task`
  и HTTP-запрос (`POST`).
- `app/tools/task_api_tool.py:75` — отладочный вывод `[TOOL CALL]` для
  `create_task`.
- `app/tools/task_api_tool.py:83-100` — `get_task` (`GET /tasks/{id}`),
  debug-вывод на строке 94.
- `app/tools/task_api_tool.py:102-121` — `update_task_status`
  (`PATCH`), debug-вывод на строке 115.
- `app/tools/task_api_tool.py:123-146` — `list_tasks` (`GET /tasks`),
  debug-вывод на строке 140.
- `app/tools/task_api_tool.py:148-162` — `get_task_stats` (`GET /stats`),
  debug-вывод на строке 156.
- `app/tools/task_api_tool.py:36-58` — обработка ответа/исключений
  (`_handle_response`, `_handle_exception`).
- `app/tools/task_api_tool.py:164-170` — экспорт списка `TASK_TOOLS`.

## Использованные промпты

См. [`prompts/used_prompts.md`](prompts/used_prompts.md).

## Результаты тестирования

См. [`tests/manual_test_results.md`](tests/manual_test_results.md).

## Выводы

TODO.
