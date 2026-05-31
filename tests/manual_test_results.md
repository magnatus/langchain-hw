# Manual Test Results

> Final manual verification of the homework project — natural-language requests
> driven through the LangChain agent against the local FastAPI Task API.

## Run metadata

| Field | Value |
|-------|-------|
| Test date | 2026-05-31 |
| LLM provider | Ollama |
| Model | `qwen3:8b` |
| API base URL | `http://localhost:8000` |

### Commands

Start the API (terminal 1):

```bash
uv run uvicorn app.api:app --reload
```

Run the agent (terminal 2), one request per invocation:

```bash
uv run python main.py "<user request>"
```

## Summary

| # | User request | Expected tool/API | Tool called? | Contract followed? | Result |
|---|--------------|-------------------|--------------|--------------------|--------|
| 1 | создай заявку: не работает VPN, приоритет высокий | `create_task -> POST /tasks` | yes | yes | ✅ passed |
| 2 | покажи заявку 1 | `get_task -> GET /tasks/1` | yes | yes | ✅ passed |
| 3 | переведи заявку 1 в статус in_progress | `update_task_status -> PATCH /tasks/1/status` | yes | yes | ✅ passed |
| 4 | покажи все заявки | `list_tasks -> GET /tasks` | yes | yes | ✅ passed |
| 5 | сколько заявок по статусам? | `get_task_stats -> GET /stats` | yes | yes | ✅ passed |
| 6 | расскажи анекдот | none (unsupported) | no | yes | ✅ passed |

- **6 scenarios executed**, **5 caused real API tool calls**, **1 unsupported**
  scenario returned `Status: error` without calling any tool.
- All scenarios produced a final response in the fixed contract.

---

## Test 1 — Create task

- **User request:** `создай заявку: не работает VPN, приоритет высокий`
- **Expected tool/API:** `create_task -> POST /tasks`
- **Command:** `uv run python main.py "создай заявку: не работает VPN, приоритет высокий"`
- **Captured tool call:**

```text
[TOOL CALL] create_task -> POST http://localhost:8000/tasks payload={'title': 'не работает VPN', 'priority': 'high', 'description': ''}
```

- **Actual output:**

```text
Status: success
Action: create task
Data: {"id": 1, "title": "не работает VPN", "priority": "high", "status": "new"}
Errors: none
```

- **Contract followed:** yes
- **Result:** ✅ passed

## Test 2 — Get task

- **User request:** `покажи заявку 1`
- **Expected tool/API:** `get_task -> GET /tasks/1`
- **Command:** `uv run python main.py "покажи заявку 1"`
- **Captured tool call:**

```text
[TOOL CALL] get_task -> GET http://localhost:8000/tasks/1
```

- **Actual output:**

```text
Status: success
Action: get task 1
Data: {"id": 1, "title": "не работает VPN", "priority": "high", "description": "", "status": "new", "created_at": "2026-05-31T15:24:33.819715+00:00"}
Errors: none
```

- **Contract followed:** yes
- **Result:** ✅ passed

## Test 3 — Update task status

- **User request:** `переведи заявку 1 в статус in_progress`
- **Expected tool/API:** `update_task_status -> PATCH /tasks/1/status`
- **Command:** `uv run python main.py "переведи заявку 1 в статус in_progress"`
- **Captured tool call:**

```text
[TOOL CALL] update_task_status -> PATCH http://localhost:8000/tasks/1/status payload={'status': 'in_progress'}
```

- **Actual output:**

```text
Status: success
Action: update task status
Data: {"id": 1, "title": "не работает VPN", "priority": "high", "description": "", "status": "in_progress", "created_at": "2026-05-31T15:24:33.819715+00:00"}
Errors: none
```

- **Contract followed:** yes
- **Result:** ✅ passed

## Test 4 — List tasks

- **User request:** `покажи все заявки`
- **Expected tool/API:** `list_tasks -> GET /tasks`
- **Command:** `uv run python main.py "покажи все заявки"`
- **Captured tool call:**

```text
[TOOL CALL] list_tasks -> GET http://localhost:8000/tasks params={}
```

- **Actual output:**

```text
Status: success
Action: listed all tasks
Data: [{"id": 1, "title": "не работает VPN", "priority": "high", "description": "", "status": "in_progress", "created_at": "2026-05-31T15:24:33.819715+00:00"}]
Errors: none
```

- **Contract followed:** yes
- **Result:** ✅ passed

## Test 5 — Get task statistics

- **User request:** `сколько заявок по статусам?`
- **Expected tool/API:** `get_task_stats -> GET /stats`
- **Command:** `uv run python main.py "сколько заявок по статусам?"`
- **Captured tool call:**

```text
[TOOL CALL] get_task_stats -> GET http://localhost:8000/stats
```

- **Actual output:**

```text
Status: success
Action: get task stats
Data: {"total": 1, "by_status": {"in_progress": 1}, "by_priority": {"high": 1}}
Errors: none
```

- **Contract followed:** yes
- **Result:** ✅ passed

## Test 6 — Unsupported request

- **User request:** `расскажи анекдот`
- **Expected behavior:** no API tool call; final response uses the fixed
  contract with `Status: error`.
- **Command:** `uv run python main.py "расскажи анекдот"`
- **Captured tool call:** none (no `[TOOL CALL]` line emitted)
- **Actual output:**

```text
Status: error
Action: unsupported request
Data: null
Errors: I can't assist with jokes. Available functions: create_task, get_task, update_task_status, list_tasks, get_task_stats.
```

- **Contract followed:** yes
- **Result:** ✅ passed

---

## Notes

- All runs used model `qwen3:8b` via Ollama, consistent with `.env`
  (`OLLAMA_MODEL=qwen3:8b`).
- Tasks share an in-memory store within a single API process, so the `id`
  values are consistent across tests 1–5 (task `1` created in test 1 is
  visible in tests 2–5).
- No flaky behavior observed across the run; each request selected the correct
  tool on the first attempt.
