# langchain-hw

A minimal LangChain AI agent that acts as a natural-language wrapper over an API.

> ⚠️ **Work in progress.** This README is a placeholder and will be completed in a later step.

## Overview

The agent accepts a natural-language request, interprets the user's intent,
calls one or more API methods through LangChain tools, and returns a structured
response with execution status.

- **LLM provider:** Ollama (default)
- **API domain:** local FastAPI mock service
- **Dependency management:** [`uv`](https://docs.astral.sh/uv/)

## Quick start (planned)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Start the mock API
uv run uvicorn app.api:app --reload

# 3. Run the agent
uv run python main.py "создай заявку: не работает VPN, приоритет высокий"
```

## Mock Task API

A local, in-memory FastAPI helpdesk/task management service that the agent
calls through LangChain tools.

### Start the API

```bash
uv run uvicorn app.api:app --reload
```

### Open interactive docs

```text
http://localhost:8000/docs
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API name and available endpoints |
| `GET` | `/health` | Health check |
| `POST` | `/tasks` | Create a task |
| `GET` | `/tasks` | List tasks (filter by `status`, `priority`) |
| `GET` | `/tasks/{task_id}` | Get a task by id |
| `PATCH` | `/tasks/{task_id}/status` | Update a task status |
| `GET` | `/stats` | Task statistics |

Allowed statuses: `new`, `in_progress`, `resolved`, `closed` (default: `new`).

### Test with curl

```bash
# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "VPN не работает", "priority": "high", "description": "Не подключается из дома"}'

# List all tasks (optionally filter)
curl http://localhost:8000/tasks
curl "http://localhost:8000/tasks?status=new&priority=high"

# Get a task by id
curl http://localhost:8000/tasks/1

# Update a task status
curl -X PATCH http://localhost:8000/tasks/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'

# Statistics
curl http://localhost:8000/stats
```

## Project structure

```text
app/        application code (api, agent, cli, tools)
prompts/    system / user prompt templates and prompt log
tests/      manual test results
```

TODO: full setup, configuration, and usage documentation.
