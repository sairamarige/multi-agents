"""Mini AI Assistant Agent — a LangGraph multi-agent system.

    START -> Router -> {Calculator | Python | General} -> Reflection -> END
                              ^                                |
                              |________ retry (<= MAX_RETRIES) _|

Public API re-exported here for convenience:
    from mini_agent import ask, app, get_active_provider, MAX_RETRIES, MEMORY_WINDOW
"""

from .config import GROQ_MODEL, MAX_RETRIES, MAX_TOOL_ITERATIONS, MEMORY_WINDOW, logger
from .graph import app, ask, build_graph
from .llm_client import get_active_provider
from .tools import TOOL_EXECUTORS, TOOL_SCHEMAS

__all__ = [
    "ask", "app", "build_graph",
    "get_active_provider",
    "GROQ_MODEL", "MAX_RETRIES", "MAX_TOOL_ITERATIONS", "MEMORY_WINDOW",
    "TOOL_EXECUTORS", "TOOL_SCHEMAS",
    "logger",
]
