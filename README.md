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

## Project structure

```text
app/        application code (api, agent, cli, tools)
prompts/    system / user prompt templates and prompt log
tests/      manual test results
```

TODO: full setup, configuration, and usage documentation.
