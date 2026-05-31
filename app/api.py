"""Local FastAPI mock API representing the task/ticket domain.

This is a placeholder mock service. The agent talks to this API through
LangChain tools instead of a real external system.

Run with:
    uv run uvicorn app.api:app --reload

TODO: implement persistent storage, validation, and richer endpoints.
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Task API (mock)", version="0.1.0")

# In-memory placeholder store. Replaced with real logic in a later step.
_TASKS: list[dict] = []


class TaskCreate(BaseModel):
    """Incoming payload for creating a task."""

    title: str
    priority: str = "normal"


class Task(BaseModel):
    """Stored task representation."""

    id: int
    title: str
    priority: str
    status: str = "open"


@app.get("/health")
def health() -> dict:
    """Simple health check."""
    return {"status": "ok"}


@app.post("/tasks", response_model=Task)
def create_task(payload: TaskCreate) -> Task:
    """Create a new task. TODO: real validation and storage."""
    task = Task(
        id=len(_TASKS) + 1,
        title=payload.title,
        priority=payload.priority,
    )
    _TASKS.append(task.model_dump())
    return task


@app.get("/tasks")
def list_tasks() -> list[dict]:
    """List all tasks. TODO: pagination and filtering."""
    return _TASKS
