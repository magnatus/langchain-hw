"""LangChain tools wrapping the local FastAPI Task API.

Each tool performs a real HTTP call to the mock API (see `app/api.py`) using
`requests`, prints a `[TOOL CALL]` debug line before the request, and returns
a JSON string describing the result.

Manual debug run:
    uv run python -m app.tools.task_api_tool
"""

from __future__ import annotations

import json
import os

import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

DEFAULT_BASE_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 10


def _api_base_url() -> str:
    """Return the Task API base URL from the environment (or the default)."""
    return os.getenv("TASK_API_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _to_json_string(data: object) -> str:
    """Serialize a Python object to a compact, UTF-8-friendly JSON string."""
    return json.dumps(data, ensure_ascii=False)


def _handle_response(response: requests.Response) -> str:
    """Convert an HTTP response into a structured JSON string.

    On a 2xx response returns ``{"ok": true, "data": ...}``; otherwise returns
    ``{"ok": false, "error": ..., "status_code": ...}``.
    """
    if response.ok:
        return _to_json_string({"ok": True, "data": response.json()})

    try:
        error = response.json()
    except ValueError:
        error = response.text
    return _to_json_string(
        {"ok": False, "error": error, "status_code": response.status_code}
    )


def _handle_exception(exc: Exception) -> str:
    """Convert a request exception into a structured JSON string."""
    return _to_json_string(
        {"ok": False, "error": str(exc), "exception_type": type(exc).__name__}
    )


@tool
def create_task(title: str, priority: str = "normal", description: str = "") -> str:
    """Create a new task. Maps to POST /tasks.

    Args:
        title: Short title of the task (required).
        priority: Task priority, e.g. "low", "normal", "high".
        description: Optional longer description of the task.

    Returns:
        A JSON string with the API response.
    """
    url = f"{_api_base_url()}/tasks"
    payload = {"title": title, "priority": priority, "description": description}
    print(f"[TOOL CALL] create_task -> POST {url} payload={payload}")
    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        return _handle_exception(exc)
    return _handle_response(response)


@tool
def get_task(task_id: int) -> str:
    """Fetch a single task by its id. Maps to GET /tasks/{task_id}.

    Args:
        task_id: The numeric id of the task to retrieve.

    Returns:
        A JSON string with the API response.
    """
    url = f"{_api_base_url()}/tasks/{task_id}"
    print(f"[TOOL CALL] get_task -> GET {url}")
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        return _handle_exception(exc)
    return _handle_response(response)


@tool
def update_task_status(task_id: int, status: str) -> str:
    """Update a task's status. Maps to PATCH /tasks/{task_id}/status.

    Args:
        task_id: The numeric id of the task to update.
        status: New status: "new", "in_progress", "resolved" or "closed".

    Returns:
        A JSON string with the API response.
    """
    url = f"{_api_base_url()}/tasks/{task_id}/status"
    payload = {"status": status}
    print(f"[TOOL CALL] update_task_status -> PATCH {url} payload={payload}")
    try:
        response = requests.patch(url, json=payload, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        return _handle_exception(exc)
    return _handle_response(response)


@tool
def list_tasks(status: str | None = None, priority: str | None = None) -> str:
    """List tasks, optionally filtered. Maps to GET /tasks.

    Args:
        status: Optional status filter.
        priority: Optional priority filter.

    Returns:
        A JSON string with the API response.
    """
    url = f"{_api_base_url()}/tasks"
    params: dict[str, str] = {}
    if status is not None:
        params["status"] = status
    if priority is not None:
        params["priority"] = priority
    print(f"[TOOL CALL] list_tasks -> GET {url} params={params}")
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        return _handle_exception(exc)
    return _handle_response(response)


@tool
def get_task_stats() -> str:
    """Get aggregated task statistics. Maps to GET /stats.

    Returns:
        A JSON string with the API response.
    """
    url = f"{_api_base_url()}/stats"
    print(f"[TOOL CALL] get_task_stats -> GET {url}")
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.RequestException as exc:
        return _handle_exception(exc)
    return _handle_response(response)


TASK_TOOLS = [
    create_task,
    get_task,
    update_task_status,
    list_tasks,
    get_task_stats,
]


if __name__ == "__main__":
    # Quick manual smoke test against a running API (uvicorn app.api:app).
    # `.invoke({...})` is how LangChain tools are called programmatically.
    print(create_task.invoke({"title": "VPN не работает", "priority": "high"}))
    print(list_tasks.invoke({}))
    print(get_task_stats.invoke({}))
