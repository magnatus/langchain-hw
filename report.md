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

## Использованные промпты

См. [`prompts/used_prompts.md`](prompts/used_prompts.md).

## Результаты тестирования

См. [`tests/manual_test_results.md`](tests/manual_test_results.md).

## Выводы

TODO.
