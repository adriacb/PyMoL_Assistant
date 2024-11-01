import json
from src.prompts import *
from src.models import *
from src.dag.tools import *
from src.dag.states import *
from src.dag.llm import model

from typing import Literal
from langchain_core.messages import (
    BaseMessage, 
    AIMessage, 
    ToolMessage,
    SystemMessage,    
)
from langchain_core.runnables import RunnableLambda

index = -2 # The index of the last message in the state (excluding the ToolMessage)

map_str_to_tool = {
    "rag_search_pymol_docs": rag_search_pymol_docs,
    "FinalResponse": FinalResponse
    }

def _invoke_tool(tool_call):

    tool = map_str_to_tool[tool_call["name"]]
    return ToolMessage(
        tool.invoke(tool_call["args"]), 
        tool_call_id=tool_call["id"]
        )

tool_executor = RunnableLambda(_invoke_tool)


def call_tools(state):
    """Execute batch tool calls and avoid duplicate ToolMessage entries."""
    last_message = state["messages"][index]
    tool_messages = tool_executor.batch(last_message.tool_calls)

    # Filter out duplicate ToolMessage entries
    new_messages = []
    for tool_msg in tool_messages:
        if all(
            not hasattr(msg, "tool_call_id") or tool_msg.tool_call_id != msg.tool_call_id
            for msg in state["messages"]
        ):
            new_messages.append(tool_msg)
    
    # Append only unique tool messages to prevent duplicates
    return {"messages": state["messages"] + new_messages}

# Define the function that determines whether to continue or not
def should_continue(state: AgentState) -> Literal["continue", "end"]: 

    messages = state['messages']
    if messages[index].tool_calls and messages[index].tool_calls[0]['name'] == 'FinalResponse':
        return "end"

    return "continue"
             

# Define the function that calls the model
async def call_model(state: AgentState) -> dict:
    """This function should handle the model invocation and tool response."""
    messages = state["messages"]

    ai_msg = await model.ainvoke(messages)
    # Check for a tool call request
    if ai_msg.tool_calls:
        # Only add ToolMessage after tool invocation
        tool_call = ai_msg.tool_calls[0]

        tool_msg = ToolMessage(
            content=tool_call['args'],
            tool_call_id=tool_call['id']
        )
        # Update state messages with tool message
        return {
            "count": state["count"] + 1,
            "messages": messages + [ai_msg, tool_msg]
        }
    # Return assistant's message if no tool call
    return {
        "count": state["count"] + 1,
        "messages": messages + [ai_msg]
    }


def respond(state: AgentState) -> dict:
    """Handles the tool response."""
    try:
        # Access tool args safely
        tool_response = state["messages"][index].tool_calls[0].get("args", {})
        if isinstance(tool_response, str):
            tool_response = json.loads(tool_response)  # Convert string to dict if necessary
        response = FinalResponse(**tool_response)

        response_message = AIMessage(content=str(response))
        return {
            "count": state["count"] + 1,
            "messages": state["messages"] + [response_message]
        }
    except Exception as e:
        print(f"Error in respond: {e}")
        return {"error": str(e)}