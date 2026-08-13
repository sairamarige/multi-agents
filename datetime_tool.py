"""Tool 5 (new): current_datetime — returns the current date/time, optionally
in a given IANA timezone. Uses the stdlib `zoneinfo` (Python 3.9+), no extra
dependency. Deterministic and offline — useful since the model itself has
no reliable sense of "now".
"""

from datetime import datetime
from typing import Any, Dict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def get_current_datetime(timezone: str = "UTC") -> str:
    try:
        tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        raise ValueError(
            f"Unknown timezone '{timezone}'. Use an IANA name, e.g. 'UTC', "
            "'America/New_York', 'Asia/Kolkata', 'Europe/London'."
        )
    now = datetime.now(tz)
    return now.strftime("%A, %Y-%m-%d %H:%M:%S %Z")


def tool_current_datetime(tool_input: Dict[str, Any]) -> str:
    try:
        timezone = tool_input.get("timezone") or "UTC"
        return get_current_datetime(timezone)
    except Exception as e:
        return f"Datetime error: {e}"


SCHEMA = {
    "name": "current_datetime",
    "description": (
        "Get the current date and time, optionally in a specific IANA "
        "timezone (e.g. 'America/New_York', 'Asia/Kolkata'). Defaults to "
        "UTC if no timezone is given. Use this whenever the current date/"
        "time/day-of-week is needed — never guess it."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "IANA timezone name, e.g. 'UTC', 'Asia/Kolkata'. Optional.",
            }
        },
        "required": [],
    },
}
