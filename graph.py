"""Builds the LangGraph state machine and exposes the top-level `ask()`
entry point every interface (CLI, Streamlit) calls through."""

from typing import List, Optional

from langgraph.graph import StateGraph, START, END

from .agents import calculator_agent, python_agent, general_agent
from .config import logger
from .reflection import reflection_agent, after_reflection
from .router import router, route_task
from .state import AgentState


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router)
    graph.add_node("calculator", calculator_agent)
    graph.add_node("python", python_agent)
    graph.add_node("general", general_agent)
    graph.add_node("reflection", reflection_agent)

    graph.add_edge(START, "router")

    graph.add_conditional_edges(
        "router",
        route_task,
        {"calculator": "calculator", "python": "python", "general": "general"},
    )

    graph.add_edge("calculator", "reflection")
    graph.add_edge("python", "reflection")
    graph.add_edge("general", "reflection")

    graph.add_conditional_edges(
        "reflection",
        after_reflection,
        {"calculator": "calculator", "python": "python", "general": "general", "end": END},
    )

    return graph.compile()


app = build_graph()


def ask(
    user_input: str, history: Optional[List[str]] = None, api_key: Optional[str] = None
) -> AgentState:
    """Runs one full turn through the graph. Wrapped in error handling so a
    truly unexpected exception can never crash the caller — it comes back
    as a normal error response.

    `api_key`, if given, is used instead of the GROQ_API_KEY env var for
    this call only — this is what lets a multi-user frontend keep each
    visitor's own key scoped to their session instead of mutating a
    process-global environment variable every concurrent user would
    otherwise share."""
    initial_state: AgentState = {
        "user_input": user_input,
        "original_input": user_input,
        "intent": "",
        "router_mode": "",
        "result": "",
        "final_response": "",
        "error": "",
        "history": history or [],
        "tool_trace": [],
        "retry_count": 0,
        "needs_retry": False,
        "api_key": api_key,
    }
    try:
        return app.invoke(initial_state)
    except Exception as e:
        logger.error(f"Unhandled error running graph for input '{user_input}': {e}")
        initial_state["final_response"] = f"⚠️ Unexpected error: {e}"
        initial_state.setdefault("history", []).append(
            f"[error] {user_input} -> {initial_state['final_response']}"
        )
        return initial_state
