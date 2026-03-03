"""
Vanilla AI Agent - A simple tool-using LLM agent implementation.
"""

import json
import os
from openai import OpenAI
from tools import TOOLS, TOOL_FUNCTIONS


def create_agent(model: str = "openrouter/free", system_prompt: str = None, enable_reasoning: bool = True):
    """Create an agent instance with the specified model and system prompt."""
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    default_system = """You are a helpful AI assistant with access to tools.
Use the available tools to help answer user questions.
Think step by step and use tools when needed to gather information or perform actions.
Always provide clear, concise responses.

## Weather Skill
When a user asks about weather:
- If NO location is provided, ask: "Which location would you like the weather for?"
- If location IS provided, use web_search to find current weather for that location."""

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
                tool_args = json.loads(tool_call.function.arguments)
                
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
