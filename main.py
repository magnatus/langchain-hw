"""Main entrypoint for the minimal LangChain API agent.

Usage:
    uv run python main.py "создай заявку: не работает VPN, приоритет высокий"
"""

from app.cli import main

if __name__ == "__main__":
    main()
