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

## LLM / модель

- **Провайдер LLM:** Ollama.
- **Модель:** `qwen3:8b`.
- Модель задаётся через переменную окружения `OLLAMA_MODEL`
  (значение по умолчанию в коде и в `.env.example` — `qwen3:8b`).
- `.env.example` содержит только безопасные примерные значения.
- Файл `.env` игнорируется git и **не должен коммититься**.
- Финальную ручную проверку домашнего задания следует выполнять с `qwen3:8b`.

## Агент и CLI

Агент реализован на LangChain 1.x с использованием `create_agent` и провайдера
**Ollama** (`langchain-ollama.ChatOllama`). Модель и провайдер настраиваются
через переменные окружения `OLLAMA_MODEL` (по умолчанию `qwen3:8b`)
и `LLM_PROVIDER` (по умолчанию `ollama`); `.env` загружается через
`python-dotenv`.

Агент:

1. принимает запрос на естественном языке;
2. интерпретирует намерение пользователя;
3. при необходимости вызывает подходящий инструмент из `TASK_TOOLS`
   (реальный HTTP-запрос к локальному API);
4. возвращает финальный ответ строго по фиксированному контракту.

Запросы, не относящиеся к операциям с задачами, не вызывают инструментов и
возвращаются с `Status: error`.

**Контракт ответа** задаётся в системном промпте и используется во всех
ответах агента:

```text
Status: success | error
Action: <short description of what was done or attempted>
Data: <structured API result or null>
Errors: <error details or none>
```

CLI (`app/cli.py`) разбирает аргументы командной строки, при отсутствии запроса
печатает usage и завершается с кодом 1, а при исключениях возвращает контракт
с `Status: error` без вывода трассировки стека. Точка входа — `main.py`,
которая вызывает `app.cli.main()`.

### Ссылки на строки кода

(Актуально на момент реализации; обновлять при изменении файлов.)

- `app/agent.py:33-52` — создание агента (`build_agent`, вызов `create_agent`).
- `app/agent.py:55-64` — запуск агента (`run_agent`, `agent.invoke`).
- `app/agent.py:28-30` — загрузка системного промпта (`load_system_prompt`).
- `app/cli.py:24-40` — запуск из CLI (разбор аргументов, вызов `run_agent`,
  обработка ошибок).
- `prompts/system.md:31-40` — контракт ответа (response contract).

## Использованные промпты

См. [`prompts/used_prompts.md`](prompts/used_prompts.md).

## Результаты тестирования

См. [`tests/manual_test_results.md`](tests/manual_test_results.md).

## Manual verification summary

- **6 сценариев выполнено** (дата прогона: 2026-05-31, модель `qwen3:8b`).
- **5 сценариев вызвали реальные обращения к API** через инструменты
  (`create_task`, `get_task`, `update_task_status`, `list_tasks`,
  `get_task_stats`).
- **1 неподдерживаемый сценарий** (`расскажи анекдот`) вернул `Status: error`
  без вызова инструментов.
- Все успешные API-сценарии вернули ответ в фиксированном контракте.

Пример:

```text
Natural-language request:
создай заявку: не работает VPN, приоритет высокий

Expected API method:
create_task -> POST /tasks

Actual debug evidence:
[TOOL CALL] create_task -> POST http://localhost:8000/tasks payload={'title': 'не работает VPN', 'priority': 'high', 'description': ''}

Result:
Status: success
```

Полные результаты по каждому сценарию — в
[`tests/manual_test_results.md`](tests/manual_test_results.md).

## Выводы

TODO.
