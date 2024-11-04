import json
from src.prompts import *
from src.models import *
from src.dag.tools import *
from src.dag.states import *
from src.dag.llm import model

from typing import Literal
from langchain_core.messages import ToolMessage, SystemMessage

from langchain_core.runnables import RunnableLambda

map_str_to_tool = {
    "rag_search_pymol_docs": rag_search_pymol_docs,
}

def _invoke_tool(tool_call):
    tool = map_str_to_tool[tool_call["name"]]
    result = tool.invoke(tool_call["args"])  # Assume this returns the result directly
    return ToolMessage(content=result, tool_call_id=tool_call["id"])

tool_executor = RunnableLambda(_invoke_tool)

def call_tools(state):
    last_message = state["messages"][-1]  # Get the last message

    # Ensure the last message has tool calls
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        tool_call = last_message.tool_calls[0]  # Process only the first tool call
        tool_result = tool_executor.invoke(tool_call)  # Invoke the tool
        
        # Construct a ToolMessage with the tool result
        tool_result_message = ToolMessage(
            content=tool_result.content,  # Assuming content is structured appropriately
            tool_call_id=tool_call["id"]
        )

        # Append the tool result to the message stack
        return {
            "messages": state["messages"] + [tool_result_message]  # Add tool result as a ToolMessage
        }

    return {
        "messages": state["messages"]  # No tool calls to process
    }

def should_continue(state) -> Literal["continue", "end"]: 
    messages = state['messages']
    if messages[-1].tool_calls and messages[-1].tool_calls[0]['name'] == 'FinalResponse':
        return "end"
    return "continue"
           
async def call_model(state) -> dict:
    messages = state["messages"]

    if len(messages) == 1:
        messages.insert(0, SystemMessage(content=SYSTEM_MESSAGE_PROMPT))
    print(f"Messages: {messages}")
    # Call the model with the structured messages
    ai_msg = await model.ainvoke(messages)

    return {
        "count": state["count"] + 1,
        "messages": messages + [ai_msg]  # Append AI response to messages
    }

def respond(state: AgentState) -> dict:
    """Handles the tool response."""
    tool_response = state["messages"][-1].tool_calls[0].get("args", {})
    
    # Construct ToolMessage
    tool_result_message = ToolMessage(
        content={"answer": tool_response["answer"]},  # Ensure this is structured as needed
        tool_call_id=state["messages"][-1].tool_calls[0]["id"]
    )

    return {
        "count": state["count"] + 1,
        "messages": state["messages"] + [tool_result_message]  # Append the ToolMessage
    }

