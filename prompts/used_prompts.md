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
