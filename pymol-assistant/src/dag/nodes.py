from src.dag.llm import model
from src.prompts import *

from typing import Literal
from langgraph.graph import MessagesState, END
from langchain.schema import (
    SystemMessage,    # Generic system message
    HumanMessage,     # HumanMessage is a message from the human
)
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableConfig

########### Short-term memory for the chat history ###########
# https://python.langchain.com/docs/versions/migrating_memory/chat_history/
chats_by_session_id: dict[str, InMemoryChatMessageHistory] = {}

def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    chat_history = chats_by_session_id.get(session_id)
    if chat_history is None:
        chat_history = InMemoryChatMessageHistory()
        chats_by_session_id[session_id] = chat_history
    return chat_history

session_id = uuid.uuid4()


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
    # Get the chat history for the session
    chat_history = get_chat_history(config.get("configurable").get("session_id"))
    
    messages = state['messages']
    
    last_message = messages[-1]
    prompt_input_messages = [
        SystemMessage(content=SYSTEM_MESSAGE_PROMPT),
        HumanMessage(content=last_message.content),
    ]
    response = model.invoke(prompt_input_messages)
    return {
        "messages": [response] # We return a list, because this will get added to the existing list
            }

# Define the function that calls the model
def call_model(state: dict) -> str:
    
    messages = state['messages']
    
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