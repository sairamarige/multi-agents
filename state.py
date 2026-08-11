"""LangGraph shared state definition."""

from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict):
    user_input: str
    original_input: str          # kept unmodified even if retries annotate user_input
    intent: str
    router_mode: str             # "llm" or "keyword-fallback"
    result: str
    final_response: str
    error: str
    history: List[str]           # short-term conversation memory
    tool_trace: List[Dict[str, Any]]  # every tool call made this turn
    retry_count: int
    needs_retry: bool
    api_key: Optional[str]       # explicit per-call key; falls back to GROQ_API_KEY env var if None
