import os
import subprocess
import sys
import tempfile
from typing import Any, Dict


def run_python_snippet(code: str, timeout: int = 5) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        output = (proc.stdout + proc.stderr).strip()
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Execution timed out after {timeout}s."
    finally:
        os.unlink(path)


def tool_code_executor(tool_input: Dict[str, Any]) -> str:
    try:
        return run_python_snippet(tool_input["code"])
    except Exception as e:
        return f"Code execution error: {e}"


SCHEMA = {
    "name": "code_executor",
    "description": (
        "Run a short Python snippet in an isolated subprocess (5s timeout) "
        "and return its stdout/stderr. Use to verify code behavior or "
        "compute something programmatically."
    ),
    "parameters": {
        "type": "object",
        "properties": {"code": {"type": "string", "description": "Python source to execute"}},
        "required": ["code"],
    },
}
