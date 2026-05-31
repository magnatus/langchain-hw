# Used Prompts

This file contains prompts used during the development of the homework project.

## Prompt 1 — Project scaffold

Date: 2026-05-31

Purpose: Create the initial project scaffold for a minimal LangChain API agent.

Prompt:

```text
We need to implement a homework project: a minimal LangChain AI agent that acts as a natural-language wrapper over an API.

The current repository is already created and cloned locally. Repository name: `langchain-hw`.

The project uses `uv` for Python dependency and environment management. Do not create a venv manually. Do not use requirements.txt as the primary dependency file. Keep dependencies in `pyproject.toml`.

Do not create an extra nested project folder. Create the project files directly in the repository root.

Project goal:
Build a small Python project where a user can run a CLI command like:

uv run python main.py "создай заявку: не работает VPN, приоритет высокий"

The agent should:

1. accept a natural language request;
2. interpret the user's intent;
3. call one or more API methods through LangChain tools;
4. return a structured response with execution status.

Use this project structure:

app/
  __init__.py
  api.py
  agent.py
  cli.py
  tools/
    __init__.py
    task_api_tool.py
prompts/
  system.md
  user_templates.md
  used_prompts.md
tests/
  manual_test_results.md
.env.example
.gitignore
README.md
report.md
main.py
pyproject.toml

For this first step, only create the project scaffold and initial files.

Requirements:

* Use Python.
* Use LangChain.
* Use Ollama as the default LLM provider.
* Use a local FastAPI mock API as the API domain.
* Do not implement full logic yet unless it is trivial placeholder code.
* Add a proper `.gitignore` that excludes `.env`, `.venv`, caches, logs, Python build artifacts, and uv cache/build artifacts if appropriate.
* Use existing `pyproject.toml` if it already exists.
* Ensure dependencies are represented in `pyproject.toml`:

  * langchain
  * langchain-ollama
  * fastapi
  * uvicorn
  * requests
  * python-dotenv
  * pydantic
* Add `.env.example` with:

  * LLM_PROVIDER=ollama
  * OLLAMA_MODEL=qwen2.5:7b-instruct
  * TASK_API_BASE_URL=http://localhost:8000
* Add short placeholder content to README.md and report.md, but make it clear that they will be completed later.
* Add placeholder prompts to `prompts/system.md` and `prompts/user_templates.md`.

Important prompt tracking requirement:

* Create `prompts/used_prompts.md`.
* This file will be used for the homework submission section "Использованные промпты".
* Add this exact prompt to `prompts/used_prompts.md` as the first entry.
* Format it in Markdown.
* Use this structure:

# Used Prompts

This file contains prompts used during the development of the homework project.

## Prompt 1 — Project scaffold

Date: YYYY-MM-DD

Purpose: Create the initial project scaffold for a minimal LangChain API agent.

Prompt:

<full prompt text here>

- Replace `YYYY-MM-DD` with the current date.
- For the full prompt text, include the full content of this instruction message.
- In future development steps, every implementation prompt must be appended to this same file as a new numbered section.
- Do not store secrets or environment values containing real credentials in this file.

Main entrypoint:
- Add a minimal `main.py` placeholder that imports from `app.cli`.
- It may contain TODOs for now, but should not crash on import if possible.

Do not commit anything.

After creating files:
1. Show the resulting tree.
2. Show a short summary of created files.
3. Confirm that `prompts/used_prompts.md` contains this prompt.
```

## Prompt 2 — Local FastAPI mock API

Date: 2026-05-31

Purpose: Implement local FastAPI mock API for task management.

Prompt:

```text
We need to continue implementing the homework project in the current repository `langchain-hw`.

Current state:

* The project scaffold already exists.
* The project uses `uv`.
* Dependencies are already defined in `pyproject.toml`.
* We must keep tracking all development prompts in `prompts/used_prompts.md`.

Task for this step:
Implement the local FastAPI mock API that the LangChain tools will call later.

API domain:
A minimal helpdesk/task management API.

Implement `app/api.py` with FastAPI.

Requirements:

1. Define a FastAPI app instance named `app`.

2. Use in-memory storage only. No database is needed.

3. Support the following operations:

   * `POST /tasks`

     * Creates a task.
     * Request body fields:

       * `title`: string, required
       * `priority`: string, optional, default `normal`
       * `description`: string, optional
     * Response should include:

       * `id`
       * `title`
       * `priority`
       * `description`
       * `status`
       * `created_at`
     * Default status: `new`.

   * `GET /tasks/{task_id}`

     * Returns a task by id.
     * If not found, return HTTP 404 with a clear error message.

   * `PATCH /tasks/{task_id}/status`

     * Updates task status.
     * Request body:

       * `status`: string, required
     * Allowed statuses:

       * `new`
       * `in_progress`
       * `resolved`
       * `closed`
     * If task is not found, return HTTP 404.
     * If status is invalid, return HTTP 400.

   * `GET /tasks`

     * Returns all tasks.
     * Optional query parameters:

       * `status`
       * `priority`
     * Filters tasks if query parameters are provided.

   * `GET /stats`

     * Returns task statistics:

       * `total`
       * `by_status`
       * `by_priority`

4. Add a root endpoint:

   * `GET /`
   * Return a simple JSON object with API name and available endpoints.

5. Add a health endpoint:

   * `GET /health`
   * Return `{"status": "ok"}`.

6. Use Pydantic models for request/response schemas where appropriate.

7. Keep the implementation simple and readable.

8. Add direct run instructions to README.md:

   * How to start API:
     `uv run uvicorn app.api:app --reload`
   * How to open docs:
     `http://localhost:8000/docs`
   * How to test with curl.

9. Add a short section to `report.md`:

   * API domain selected.
   * Supported operations.
   * Mention that the API is local and in-memory.

10. Append this full prompt as a new section in `prompts/used_prompts.md`:

Section title:
`## Prompt 2 — Local FastAPI mock API`

Include:

* Date: current date.
* Purpose: Implement local FastAPI mock API for task management.
* Full prompt text in a fenced `text` block.

11. Do not commit anything.

12. After changes, show:

* Modified files.
* A short implementation summary.
* Commands to run the API.
* One example curl command for creating a task.
```

## Prompt 3 — LangChain API tools

Date: 2026-05-31

Purpose: Implement LangChain tools with real HTTP calls to the local Task API.

Prompt:

```text
We need to continue implementing the homework project in the current repository `langchain-hw`.

Current state:

* Project scaffold exists.
* The project uses `uv`.
* Local FastAPI mock API is implemented in `app/api.py`.
* API has been manually tested:

  * `GET /health`
  * `POST /tasks`
  * `GET /tasks`
  * `GET /stats`
* We must keep tracking all development prompts in `prompts/used_prompts.md`.

Task for this step:
Implement LangChain tools that call the local FastAPI Task API through real HTTP requests.

Important homework criteria this step must satisfy:

* At least one API-tool must be implemented as a real LangChain tool.
* The tool must perform a real API call.
* The tool must print/log debug output to the console showing the tool call and API method.
* Later we need to reference file and line ranges where:

  * the tool is declared;
  * the HTTP call is executed;
  * debug output is printed.

Files to modify:

* `app/tools/task_api_tool.py`
* `README.md`
* `report.md`
* `prompts/used_prompts.md`

Implementation requirements:

1. In `app/tools/task_api_tool.py`, implement separate LangChain tools using the `@tool` decorator.

Create these tools:

* `create_task`

  * Calls `POST /tasks`
  * Input arguments:

    * `title: str`
    * `priority: str = "normal"`
    * `description: str = ""`
  * Returns a JSON string with the API response.

* `get_task`

  * Calls `GET /tasks/{task_id}`
  * Input:

    * `task_id: int`
  * Returns a JSON string with the API response.

* `update_task_status`

  * Calls `PATCH /tasks/{task_id}/status`
  * Input:

    * `task_id: int`
    * `status: str`
  * Returns a JSON string with the API response.

* `list_tasks`

  * Calls `GET /tasks`
  * Optional inputs:

    * `status: str | None = None`
    * `priority: str | None = None`
  * Returns a JSON string with the API response.

* `get_task_stats`

  * Calls `GET /stats`
  * No inputs.
  * Returns a JSON string with the API response.

2. Use `requests` for HTTP calls.

3. Read API base URL from environment variable:

   * `TASK_API_BASE_URL`
   * Default: `http://localhost:8000`

4. Load `.env` via `python-dotenv`.

5. Add helper functions if useful:

   * `_api_base_url()`
   * `_handle_response(response)`
   * `_to_json_string(data)`

6. Every tool must print a debug line before making the request.

Examples:

    print(f"[TOOL CALL] create_task -> POST {url} payload={payload}")
    print(f"[TOOL CALL] get_task -> GET {url}")

7. Error handling:

   * If API returns non-2xx, return a JSON string like:

       {
         "ok": false,
         "error": "...",
         "status_code": 404
       }

   * If request fails, return:

       {
         "ok": false,
         "error": "...",
         "exception_type": "ConnectionError"
       }

8. Successful tool response should return a JSON string like:

     {
       "ok": true,
       "data": { ... }
     }

9. Export all tools through a list:

     TASK_TOOLS = [
         create_task,
         get_task,
         update_task_status,
         list_tasks,
         get_task_stats,
     ]

10. Add a small direct debug/test block if appropriate:

     if __name__ == "__main__":
         ...

    But do not require this for normal use.

11. Update README.md:

    * Add a section "LangChain API tools".
    * List tools and corresponding HTTP API methods.
    * Mention that tool calls print debug output like `[TOOL CALL] ...`.

12. Update report.md:

    * Add a section about implemented tools.
    * Include a placeholder for line references, for example:

      * `app/tools/task_api_tool.py:Lx-Ly` — tool declaration and HTTP request
      * `app/tools/task_api_tool.py:Lx-Ly` — debug print
    * We will fill exact line numbers after implementation.

13. Append this full prompt as a new section in `prompts/used_prompts.md`:

    Section title:
    `## Prompt 3 — LangChain API tools`

    Include:

    * Date: current date.
    * Purpose: Implement LangChain tools with real HTTP calls to the local Task API.
    * Full prompt text in a fenced `text` block.

14. Do not commit anything.

15. After changes, show:

    * Modified files.
    * A short implementation summary.
    * The tool names and matching API methods.
    * How to manually test at least one tool.
```
