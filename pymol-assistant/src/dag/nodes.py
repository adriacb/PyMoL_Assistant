from src.dag.llm import model
from src.prompts import *

from typing import Literal
from langgraph.graph import MessagesState, END
from langchain.schema import (
    SystemMessage,    # Generic system message
    HumanMessage,     # HumanMessage is a message from the human
)

# Define the function that determines whether to continue or not
def should_continue(state: MessagesState) -> Literal["tools", END]:
    
    messages = state['messages']
    last_message = messages[-1]

    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END

# Define the function that calls the model
def call_model(state: dict) -> str:
    
    messages = state['messages']
    print(f"Messages: {messages}")
    last_message = messages[-1]
    prompt_input_messages = [
        SystemMessage(content=SYSTEM_MESSAGE_PROMPT),
        HumanMessage(content=last_message.content),
    ]
    response = model.invoke(prompt_input_messages)
    return {
        "messages": [response] # We return a list, because this will get added to the existing list
            }

def call_summary_model(state: dict) -> str:
    
    messages = state['messages']
    
    last_message = messages[-1]
    
    prompt_input_messages = [
        #SystemMessage(content=SYSTEM_MESSAGE_PROMPT),
        HumanMessage(content=SUMMARY_LLM_PROMPT.format(context=last_message.content)),
    ]
    response = model.invoke(prompt_input_messages)
    return {
        "messages": [response] # We return a list, because this will get added to the existing list
            }