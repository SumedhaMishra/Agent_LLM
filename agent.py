"""
Vanilla AI Agent - A simple tool-using LLM agent implementation.
"""

import json
import os
import datetime
from openai import OpenAI
from tools import TOOLS, TOOL_FUNCTIONS


def create_agent(model: str = "openrouter/free", system_prompt: str = None, enable_reasoning: bool = True):
    """Create an agent instance with the specified model and system prompt."""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    # Get current date for context
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    current_month_year = datetime.datetime.now().strftime("%B %Y")
    
    default_system = f"""You are a helpful AI assistant with access to tools.
Today's date is {current_date}.
Use the available tools to help answer user questions.
Think step by step and use tools when needed to gather information or perform actions.
Always provide clear, concise responses.

## General Output Rules
- When presenting search results or multiple items, ALWAYS use a TABLE format
- Do NOT include URLs or links in your responses
- Table format: | # | Title/Headline | Summary/Details |

## Weather & Temperature Skill
When a user asks about weather or temperature:
- If NO location is provided, ask: "Which location would you like the weather for?"
- Do NOT search until you have a location
- If location IS provided, use web_search to find current weather/temperature for that location
- Search query format: "current weather in [location]" or "current temperature in [location]"
- Present the results clearly with temperature, conditions, and relevant details.

## News & Current Affairs Skill
When a user asks about news or what happened recently:
- ALWAYS include "{current_month_year}" in your search queries to get current news
- If timeframe is specified (this week, last week, today), use web_search
- Search query format: "top news {current_month_year}" or "[topic] news {current_month_year}"
- Present results in a TABLE format: | # | Headline | Summary |
- Do NOT include URLs or links in your response
- If neither timeframe nor topic is given, ask: "Would you like news from this week, or about a specific topic?" """

    return {
        "client": client,
        "model": model,
        "system_prompt": system_prompt or default_system,
        "messages": [],
        "max_iterations": 10,
        "enable_reasoning": enable_reasoning
    }


def run_agent(agent: dict, user_input: str) -> str:
    """
    Run the agent loop for a given user input.
    
    The agent will:
    1. Send user input to the LLM
    2. If the LLM requests tool calls, execute them
    3. Send tool results back to the LLM
    4. Repeat until the LLM provides a final response
    """
    # Initialize conversation with system prompt
    messages = [
        {"role": "system", "content": agent["system_prompt"]},
        {"role": "user", "content": user_input}
    ]
    
    iteration = 0
    
    while iteration < agent["max_iterations"]:
        iteration += 1
        print(f"\n--- Agent Iteration {iteration} ---")
        
        # Build API call parameters
        api_params = {
            "model": agent["model"],
            "messages": messages,
            "tools": TOOLS,
            "tool_choice": "auto"
        }
        
        # Add reasoning support if enabled
        if agent.get("enable_reasoning", True):
            api_params["extra_body"] = {"reasoning": {"enabled": True}}
        
        # Call the LLM
        response = agent["client"].chat.completions.create(**api_params)
        
        assistant_message = response.choices[0].message
        
        # Build message dict preserving reasoning_details if present
        msg_dict = {
            "role": "assistant",
            "content": assistant_message.content
        }
        
        # Preserve reasoning_details for multi-turn reasoning
        if hasattr(assistant_message, 'reasoning_details') and assistant_message.reasoning_details:
            msg_dict["reasoning_details"] = assistant_message.reasoning_details
            print(f"  [Reasoning enabled]")
        
        # Preserve tool_calls if present
        if assistant_message.tool_calls:
            msg_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in assistant_message.tool_calls
            ]
        
        messages.append(msg_dict)
        
        # Check if there are tool calls
        if assistant_message.tool_calls:
            print(f"Tool calls requested: {len(assistant_message.tool_calls)}")
            
            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                
                # Parse tool arguments with error handling
                try:
                    tool_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                except json.JSONDecodeError as e:
                    print(f"  JSON parse error: {e}")
                    print(f"  Raw arguments: {tool_call.function.arguments}")
                    # Try to extract query from malformed JSON
                    import re
                    match = re.search(r'"query"\s*:\s*"([^"]+)"', tool_call.function.arguments or "")
                    if match:
                        tool_args = {"query": match.group(1)}
                    else:
                        tool_args = {}
                
                print(f"  Executing: {tool_name}({tool_args})")
                
                # Execute the tool
                if tool_name in TOOL_FUNCTIONS:
                    try:
                        result = TOOL_FUNCTIONS[tool_name](**tool_args)
                        tool_result = str(result)
                    except Exception as e:
                        tool_result = f"Error: {str(e)}"
                else:
                    tool_result = f"Error: Unknown tool '{tool_name}'"
                
                print(f"  Result: {tool_result[:100]}...")
                
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })
        else:
            # No tool calls - agent is done
            final_response = assistant_message.content
            print(f"\n--- Agent Complete ---")
            return final_response
    
    return "Agent reached maximum iterations without completing."


def chat_loop():
    """Run an interactive chat loop with the agent."""
    print("=" * 50)
    print("Vanilla AI Agent")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    agent = create_agent()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit"]:
                print("Goodbye!")
                break
            
            response = run_agent(agent, user_input)
            print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    chat_loop()
