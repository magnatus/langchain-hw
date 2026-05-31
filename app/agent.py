"""LangChain agent assembly.

Builds an agent backed by Ollama (via `langchain-ollama`) that interprets a
natural-language request and calls the Task API tools to satisfy it. The
agent's final answer follows the fixed response contract documented in
`prompts/system.md`.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from app.tools.task_api_tool import TASK_TOOLS

load_dotenv()

DEFAULT_MODEL = "qwen3:8b"
DEFAULT_PROVIDER = "ollama"

_SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "system.md"


def load_system_prompt() -> str:
    """Load the agent system prompt from `prompts/system.md`."""
    return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def build_agent():
    """Build and return the LangChain agent.

    Uses Ollama as the LLM provider (configurable via `LLM_PROVIDER` /
    `OLLAMA_MODEL`) and binds the Task API tools.
    """
    provider = os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER)
    if provider != "ollama":
        raise ValueError(
            f"Unsupported LLM_PROVIDER '{provider}'. Only 'ollama' is supported."
        )

    model_name = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
    model = ChatOllama(model=model_name, temperature=0)

    return create_agent(
        model,
        TASK_TOOLS,
        system_prompt=load_system_prompt(),
    )


def run_agent(user_input: str) -> str:
    """Run the agent against a natural-language request.

    Returns the agent's final answer as plain text following the response
    contract from the system prompt.
    """
    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    messages = result["messages"]
    return messages[-1].content
