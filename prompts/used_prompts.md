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

## Prompt 4 — LangChain agent and CLI

Date: 2026-05-31

Purpose: Implement LangChain agent and CLI entrypoint.

Prompt:

```text
We need to continue implementing the homework project in the current repository `langchain-hw`.

Current state:

* The project uses `uv`.
* Local FastAPI mock API is implemented in `app/api.py`.
* LangChain tools are implemented in `app/tools/task_api_tool.py`.
* Tools call the local API through real HTTP requests.
* Tools print debug output like `[TOOL CALL] ...`.
* We must keep tracking all development prompts in `prompts/used_prompts.md`.

Task for this step:
Implement the LangChain agent and CLI entrypoint.

Homework requirements this step must satisfy:

* The agent accepts a natural-language user request.
* The agent interprets the user intent.
* The agent chooses and calls the correct API tool when appropriate.
* The final answer follows a fixed response contract.
* The agent can be launched from CLI.

Files to modify:

* `app/agent.py`
* `app/cli.py`
* `main.py`
* `prompts/system.md`
* `prompts/user_templates.md`
* `README.md`
* `report.md`
* `prompts/used_prompts.md`

Implementation requirements:

1. Use Ollama as the default LLM provider through `langchain-ollama`.

2. Read configuration from environment:

   * `OLLAMA_MODEL`
   * default: `qwen2.5:7b-instruct`
   * `LLM_PROVIDER`
   * default: `ollama`

3. Load `.env` using `python-dotenv`.

4. Use the existing tools exported as:

   * `TASK_TOOLS` from `app.tools.task_api_tool`

5. Implement `app/agent.py` with:

   * `load_system_prompt()`
   * `build_agent()`
   * `run_agent(user_input: str) -> str`

6. Prefer the current LangChain API for agent creation.

   * Use `create_agent` if available in the installed LangChain version.
   * If the installed version requires another compatible approach, use the modern recommended API for the installed version.
   * Keep the implementation simple and readable.

7. The system prompt must define the agent as an API operator.

8. The system prompt must include these rules:

   * The agent manages tasks through tools only.
   * The agent must not invent API results.
   * For create/get/update/list/stats operations, it must call the appropriate tool.
   * If the user request is unrelated to task API operations, return an error in the fixed response format.
   * Final response must strictly follow this contract:

    Status: success | error
    Action: <short description of what was done or attempted>
    Data: <structured API result or null>
    Errors: <error details or none>

9. The final answer returned to the user must be in the exact contract above.

   * Do not wrap it in Markdown.
   * Do not add extra commentary before or after the contract.

10. Implement `app/cli.py`:

    * Parse the user's request from command line arguments.
    * If no argument is provided, print usage and exit with code 1.
    * Call `run_agent(user_input)`.
    * Print the final response.
    * Keep stack traces out of normal user output; handle exceptions and return the response contract with `Status: error`.

11. Implement root `main.py`:

    * Thin entrypoint that calls `app.cli.main()`.

12. Update `prompts/system.md` with the actual system prompt used by the agent.

13. Update `prompts/user_templates.md` with example user request templates:

    * Create task
    * Get task
    * Update status
    * List tasks
    * Get stats
    * Unsupported request

14. Update README.md:

    * Add instructions for running the agent:

      * Start API:
        `uv run uvicorn app.api:app --reload`
      * In another terminal, run:
        `uv run python main.py "создай заявку: не работает VPN, приоритет высокий"`
    * Add the response contract section.
    * Add example requests.

15. Update report.md:

    * Add a section describing the agent implementation.
    * Mention where the response contract is documented.
    * Add placeholders for line references:

      * `app/agent.py:Lx-Ly` — agent creation
      * `app/cli.py:Lx-Ly` — CLI launch
      * `prompts/system.md:Lx-Ly` — response contract

16. Append this full prompt as a new section in `prompts/used_prompts.md`:

    Section title:
    `## Prompt 4 — LangChain agent and CLI`

    Include:

    * Date: current date.
    * Purpose: Implement LangChain agent and CLI entrypoint.
    * Full prompt text in a fenced `text` block.

17. Do not commit anything.

18. After changes, show:

    * Modified files.
    * Short implementation summary.
    * Exact command to run the API.
    * Exact command to run the agent.
    * One example expected output.
```

## Prompt 5 — Switch default Ollama model to qwen3:8b

Date: 2026-05-31

Purpose: Update runtime default, documentation, and setup instructions to use qwen3:8b.

Prompt:

```text
We need to update the homework project configuration, runtime fallback, documentation, and local setup instructions to use `qwen3:8b` as the default Ollama model.

Repository: `langchain-hw`.

Current state:

* The LangChain agent is already implemented.
* The project uses `uv`.
* The project uses Ollama via `langchain-ollama`.
* The previous default model may still be `qwen2.5:7b-instruct` in `.env.example`, `app/agent.py`, README, report, or prompt docs.
* The developer already has `qwen3:8b` downloaded locally and uses it in another project.
* We must keep tracking all development prompts in `prompts/used_prompts.md`.
* Do not commit anything.

Goal:
Make `qwen3:8b` the documented and runtime default model for this homework project.

Important:

* Do not commit a real `.env` file.
* `.env` must remain ignored.
* `.env.example` should be committed and should contain safe example values only.
* Do not add any secrets or real credentials.
* Do not change unrelated project behavior.

Files to inspect and update if needed:

* `.env.example`
* `.gitignore`
* `app/agent.py`
* `README.md`
* `report.md`
* `prompts/system.md`
* `prompts/user_templates.md`
* `tests/manual_test_results.md`
* `prompts/used_prompts.md`

Required changes:

1. Update default model configuration.

   In `.env.example`, set:

       LLM_PROVIDER=ollama
       OLLAMA_MODEL=qwen3:8b
       TASK_API_BASE_URL=http://localhost:8000

2. Update runtime fallback.

   Inspect `app/agent.py`.

   If there is code like:

       os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")

   change the fallback to:

       os.getenv("OLLAMA_MODEL", "qwen3:8b")

   Keep `OLLAMA_MODEL` override behavior intact.

3. Ensure local `.env` is ignored.

   Inspect `.gitignore`.

   Make sure `.env` is ignored.
   Do not add `.env` to git.
   If `.env` exists locally, leave it untracked/ignored.

4. Add or update local setup instructions.

   In `README.md`, add a clear section explaining:

   * The default LLM provider is Ollama.
   * The default model is `qwen3:8b`.
   * Check installed models: `ollama list`
   * Pull the model if missing: `ollama pull qwen3:8b`
   * Create local `.env` from `.env.example`: `cp .env.example .env`
   * `.env` is local only and must not be committed.
   * Start API: `uv run uvicorn app.api:app --reload`
   * Run agent: `uv run python main.py "создай заявку: не работает VPN, приоритет высокий"`

5. Update `report.md`.

   Add or update the LLM section:

   * LLM provider: Ollama.
   * Model: `qwen3:8b`.
   * Model configured through `OLLAMA_MODEL`.
   * `.env.example` contains safe example config.
   * `.env` is ignored and must not be committed.
   * Homework verification should be run with `qwen3:8b`.

6. Update test documentation if needed.

   If `tests/manual_test_results.md` already mentions another model, update it to `qwen3:8b`.

   If manual tests have not been run yet, add a note that final manual verification is expected to use `qwen3:8b`.

7. Update prompt/user docs if needed.

   Search the repository for the old model name:

       grep -R "qwen2.5:7b-instruct" -n . --exclude-dir=.git --exclude-dir=.venv --exclude=uv.lock

   Replace references to `qwen2.5:7b-instruct` with `qwen3:8b` where they describe the current/default model.

   Exception:

   * If old model name appears inside historical prompts in `prompts/used_prompts.md`, do not rewrite older prompt contents. Historical prompt text should remain as originally used.
   * Instead, add the new prompt section explaining the model switch.

8. Append this full prompt to `prompts/used_prompts.md`.

   Section title:

       ## Prompt 5 — Switch default Ollama model to qwen3:8b

   Include:

   * Date: current date.
   * Purpose: Update runtime default, documentation, and setup instructions to use qwen3:8b.
   * Full prompt text in a fenced `text` block.

   Important:

   * Do not edit the content of previous prompt entries.
   * Append only.

9. Validate.

   Run:

       uv run python -m compileall app

   Then show the remaining occurrences of both model names:

       grep -R "qwen2.5:7b-instruct\|qwen3:8b" -n . --exclude-dir=.git --exclude-dir=.venv --exclude=uv.lock

   Also show:

       git status --short

10. Final response after changes.

Show:

* Modified files.
* What exactly changed.
* Whether `app/agent.py` fallback was updated.
* Whether `.env` is ignored.
* Remaining occurrences of `qwen2.5:7b-instruct`, if any, and explain whether they are only historical prompt entries.
* Validation command results.
* Reminder that nothing was committed.
```
