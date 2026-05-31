"""LangChain agent assembly.

Builds an agent backed by Ollama that can call the task API tools to
satisfy a natural-language request.

TODO:
    - Load the system prompt from prompts/system.md.
    - Construct the Ollama chat model from environment configuration.
    - Bind the task API tools and build the agent executor.
    - Return a structured response with execution status.
"""

from __future__ import annotations

import os


def build_agent():
    """Build and return the LangChain agent executor.

    Placeholder: full implementation comes in a later step.
    """
    provider = os.getenv("LLM_PROVIDER", "ollama")
    model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b-instruct")
    # TODO: instantiate ChatOllama, load tools, build agent.
    raise NotImplementedError(
        f"Agent not implemented yet (provider={provider}, model={model})."
    )


def run_agent(user_request: str) -> dict:
    """Run the agent against a natural-language request.

    Returns a structured response dict. Placeholder for now.
    """
    # TODO: invoke the agent executor and normalize its output.
    return {
        "status": "not_implemented",
        "request": user_request,
        "result": None,
    }
