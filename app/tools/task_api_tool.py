"""LangChain tool(s) wrapping the mock Task API.

These tools let the agent create and query tasks via HTTP calls to the
local FastAPI mock service.

TODO:
    - Define structured-args schemas with pydantic.
    - Implement create_task / list_tasks tools using `requests`.
    - Add error handling and structured status responses.
"""

from __future__ import annotations

import os

import requests

TASK_API_BASE_URL = os.getenv("TASK_API_BASE_URL", "http://localhost:8000")


def create_task(title: str, priority: str = "normal") -> dict:
    """Create a task through the mock API. Placeholder implementation."""
    # TODO: wrap as a LangChain @tool and harden error handling.
    response = requests.post(
        f"{TASK_API_BASE_URL}/tasks",
        json={"title": title, "priority": priority},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def list_tasks() -> list[dict]:
    """List tasks through the mock API. Placeholder implementation."""
    # TODO: wrap as a LangChain @tool.
    response = requests.get(f"{TASK_API_BASE_URL}/tasks", timeout=10)
    response.raise_for_status()
    return response.json()
