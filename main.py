"""Main entrypoint for the minimal LangChain API agent.

Usage:
    uv run python main.py "создай заявку: не работает VPN, приоритет высокий"

TODO: wire up full CLI argument parsing and agent execution.
"""

from app.cli import main

if __name__ == "__main__":
    main()
