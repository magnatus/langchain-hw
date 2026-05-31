"""Command-line interface for the LangChain API agent.

Usage:
    uv run python main.py "создай заявку: не работает VPN, приоритет высокий"
"""

from __future__ import annotations

import sys

from app.agent import run_agent


def main() -> None:
    """Parse the CLI request and run the agent.

    TODO: richer argument parsing, flags, and output formatting.
    """
    if len(sys.argv) < 2:
        print('Usage: uv run python main.py "<natural language request>"')
        sys.exit(1)

    user_request = " ".join(sys.argv[1:])
    response = run_agent(user_request)
    print(response)


if __name__ == "__main__":
    main()
