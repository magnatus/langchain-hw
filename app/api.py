"""Local FastAPI mock API: a minimal helpdesk / task management service.

The agent talks to this API through LangChain tools instead of a real
external system. Storage is in-memory only — no database is required.

Run with:
    uv run uvicorn app.api:app --reload

Open docs at:
    http://localhost:8000/docs
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task API (mock)", version="0.1.0")

ALLOWED_STATUSES = ["new", "in_progress", "resolved", "closed"]
DEFAULT_STATUS = "new"

# In-memory store. Maps task id -> task dict.
_TASKS: dict[int, dict] = {}
_NEXT_ID = 1


class TaskCreate(BaseModel):
    """Incoming payload for creating a task."""

    title: str
    priority: str = "normal"
    description: str | None = None


class StatusUpdate(BaseModel):
    """Incoming payload for updating a task status."""

    status: str


class Task(BaseModel):
    """Stored task representation returned to clients."""

    id: int
    title: str
    priority: str
    description: str | None = None
    status: str = DEFAULT_STATUS
    created_at: str


class Stats(BaseModel):
    """Aggregated task statistics."""

    total: int
    by_status: dict[str, int]
    by_priority: dict[str, int]


def _now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


@app.get("/")
def root() -> dict:
    """Root endpoint: API name and available endpoints."""
    return {
        "name": "Task API (mock)",
        "endpoints": [
            "POST /tasks",
            "GET /tasks",
            "GET /tasks/{task_id}",
            "PATCH /tasks/{task_id}/status",
            "GET /stats",
            "GET /health",
        ],
    }


@app.get("/health")
def health() -> dict:
    """Simple health check."""
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    """Create a new task with default status `new`."""
    global _NEXT_ID
    task = Task(
        id=_NEXT_ID,
        title=payload.title,
        priority=payload.priority,
        description=payload.description,
        status=DEFAULT_STATUS,
        created_at=_now_iso(),
    )
    _TASKS[task.id] = task.model_dump()
    _NEXT_ID += 1
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks(
    status: str | None = None,
    priority: str | None = None,
) -> list[dict]:
    """List all tasks, optionally filtered by status and/or priority."""
    tasks = list(_TASKS.values())
    if status is not None:
        tasks = [t for t in tasks if t["status"] == status]
    if priority is not None:
        tasks = [t for t in tasks if t["priority"] == priority]
    return tasks


@app.get("/stats", response_model=Stats)
def stats() -> Stats:
    """Return task statistics: totals plus breakdowns by status and priority."""
    tasks = list(_TASKS.values())
    return Stats(
        total=len(tasks),
        by_status=dict(Counter(t["status"] for t in tasks)),
        by_priority=dict(Counter(t["priority"] for t in tasks)),
    )


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> dict:
    """Return a single task by id, or 404 if it does not exist."""
    task = _TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.patch("/tasks/{task_id}/status", response_model=Task)
def update_task_status(task_id: int, payload: StatusUpdate) -> dict:
    """Update a task's status; validate the status value and task existence."""
    task = _TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    if payload.status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid status '{payload.status}'. "
                f"Allowed: {', '.join(ALLOWED_STATUSES)}"
            ),
        )
    task["status"] = payload.status
    return task
