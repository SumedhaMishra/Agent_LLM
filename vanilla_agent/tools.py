"""
Example tools for the Vanilla AI Agent.
Add your own tools by defining a function and adding it to TOOLS and TOOL_FUNCTIONS.
"""

import datetime
import math
import requests
from duckduckgo_search import DDGS


# ============================================================================
# TOOL DEFINITIONS (OpenAI Function Calling Format)
# ============================================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Optional timezone (e.g., 'UTC', 'US/Eastern'). Defaults to local time."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform mathematical calculations. Supports basic arithmetic and common math functions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2', 'sqrt(16)', 'sin(3.14)')"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web using DuckDuckGo. Returns titles, URLs, and snippets of top results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 5)"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "http_request",
            "description": "Make an HTTP request to a URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to request"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST"],
                        "description": "HTTP method (default: GET)"
                    }
                },
                "required": ["url"]
            }
        }
    }
]


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def get_current_time(timezone: str = None) -> str:
    """Get the current date and time."""
    now = datetime.datetime.now()
    if timezone:
        try:
            import pytz
            tz = pytz.timezone(timezone)
            now = datetime.datetime.now(tz)
        except ImportError:
            return f"Current time (local): {now.strftime('%Y-%m-%d %H:%M:%S')} (pytz not installed for timezone support)"
        except Exception as e:
            return f"Error with timezone: {e}. Local time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    return now.strftime('%Y-%m-%d %H:%M:%S')


def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    # Safe math functions available for evaluation
    safe_dict = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "pow": pow,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "floor": math.floor,
        "ceil": math.ceil,
    }
    
    try:
        # Only allow safe mathematical operations
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"


def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo.
    Returns top search results with titles, URLs, and snippets.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return f"No results found for: '{query}'"
        
        output = []
        for i, r in enumerate(results, 1):
            output.append(f"{i}. {r.get('title', 'No title')}")
            output.append(f"   URL: {r.get('href', 'No URL')}")
            output.append(f"   {r.get('body', 'No description')}")
            output.append("")
        
        return "\n".join(output)
    except Exception as e:
        return f"Search error: {e}"


def read_file(file_path: str) -> str:
    """Read contents of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found"
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(file_path: str, content: str) -> str:
    """Write content to a file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to '{file_path}'"
    except Exception as e:
        return f"Error writing file: {e}"


def http_request(url: str, method: str = "GET") -> str:
    """Make an HTTP request."""
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, timeout=10)
        else:
            return f"Unsupported method: {method}"
        
        return f"Status: {response.status_code}\nContent: {response.text[:2000]}"
    except Exception as e:
        return f"Error making request: {e}"


# ============================================================================
# TOOL FUNCTION REGISTRY
# ============================================================================

TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculator": calculator,
    "web_search": web_search,
    "read_file": read_file,
    "write_file": write_file,
    "http_request": http_request,
}
