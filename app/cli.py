"""Command-line interface for the LangChain API agent.

Usage:
    uv run python main.py "создай заявку: не работает VPN, приоритет высокий"
"""

from __future__ import annotations

import sys

from app.agent import run_agent


def _error_response(action: str, error: str) -> str:
    """Build a response-contract string for a failure that occurred in the CLI."""
    return (
        "Status: error\n"
        f"Action: {action}\n"
        "Data: null\n"
        f"Errors: {error}"
    )


def main() -> None:
    """Parse the CLI request, run the agent, and print the final response."""
    if len(sys.argv) < 2 or not " ".join(sys.argv[1:]).strip():
        print('Usage: uv run python main.py "<natural language request>"')
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])

    try:
        response = run_agent(user_input)
    except Exception as exc:  # noqa: BLE001 - surface as contract, not a traceback
        response = _error_response(
            action="run agent",
            error=f"{type(exc).__name__}: {exc}",
        )

    print(response)


if __name__ == "__main__":
    main()
