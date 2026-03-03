# Vanilla AI Agent

A minimal, clean implementation of an AI agent with tool-use capabilities using OpenRouter.ai.

## Features

- **Simple Agent Loop**: Clean implementation of the core agent reasoning loop
- **Tool Support**: Built-in tools with easy extensibility
- **Reasoning Support**: OpenRouter reasoning feature for better multi-step thinking
- **Free Model**: Uses `openrouter/free` by default (no cost)
- **Interactive Chat**: Command-line chat interface
- **Configurable**: Easy to customize model, system prompt, and tools

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenRouter API key**:
   ```bash
   # Windows
   set OPENROUTER_API_KEY=your-api-key-here
   
   # Linux/Mac
   export OPENROUTER_API_KEY=your-api-key-here
   ```

3. **Run the agent**:
   ```bash
   python agent.py
   ```

## Built-in Tools

| Tool | Description |
|------|-------------|
| `get_current_time` | Get current date and time |
| `calculator` | Evaluate mathematical expressions |
| `web_search` | Search the web using DuckDuckGo (no API key needed) |
| `read_file` | Read file contents |
| `write_file` | Write content to a file |
| `http_request` | Make HTTP GET/POST requests |

## Adding Custom Tools

1. **Define the tool schema** in `tools.py`:
   ```python
   {
       "type": "function",
       "function": {
           "name": "my_tool",
           "description": "What the tool does",
           "parameters": {
               "type": "object",
               "properties": {
                   "param1": {
                       "type": "string",
                       "description": "Description of param1"
                   }
               },
               "required": ["param1"]
           }
       }
   }
   ```

2. **Implement the function**:
   ```python
   def my_tool(param1: str) -> str:
       # Your implementation
       return "result"
   ```

3. **Register in `TOOL_FUNCTIONS`**:
   ```python
   TOOL_FUNCTIONS = {
       # ... existing tools
       "my_tool": my_tool,
   }
   ```

## Usage Examples

### Interactive Chat
```bash
python agent.py
```

### Programmatic Usage
```python
from agent import create_agent, run_agent

# Default: uses openrouter/free with reasoning enabled
agent = create_agent()

# Or customize model and reasoning
agent = create_agent(
    model="openrouter/free",  # or "anthropic/claude-3-opus", "openai/gpt-4o", etc.
    system_prompt="You are a helpful assistant.",
    enable_reasoning=True  # Enables OpenRouter's reasoning feature
)

response = run_agent(agent, "What is 25 * 4?")
print(response)
```

## Architecture

```
┌────────────────┐
│   User Input   │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   Agent Loop   │ ◄─── Iterates until task complete
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   LLM (GPT)    │ ◄─── Decides what to do
└───────┬────────┘
        │
    ┌───┴───┐
    │       │
    ▼       ▼
┌──────┐ ┌──────────┐
│ Done │ │Tool Call │
└──────┘ └────┬─────┘
              │
              ▼
       ┌────────────┐
       │Execute Tool│
       └─────┬──────┘
             │
             ▼
       ┌────────────┐
       │Return Result│ ─── Back to LLM
       └────────────┘
```

## License

MIT
