from src.dag.llm import model
from src.prompts import *

from typing import Literal
from langgraph.graph import MessagesState, END
from langchain_core.messages import BaseMessage
from langchain.schema import (
    SystemMessage,    # Generic system message
    HumanMessage,     # HumanMessage is a message from the human
    AIMessage,        # AIMessage is a message from the AI
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
def call_model(state: MessagesState, config: RunnableConfig) -> list[BaseMessage]:
    # Make sure that config is populated with the session id
    if "configurable" not in config or "session_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"
        )
    # Get the chat history for the session
    chat_history = get_chat_history(config.get("configurable").get("session_id"))
    #print("1. ", chat_history.messages)
    if len(chat_history.messages) == 0:
        chat_history.add_message(SystemMessage(content=SYSTEM_MESSAGE_PROMPT))
    
    messages = list(chat_history.messages) + state['messages']

    response = model.invoke(messages)

    chat_history.add_messages(state["messages"] + [response])
    
    return {"messages": response}

def call_summary_model(state: MessagesState, config: RunnableConfig) -> list[BaseMessage]:
    """This model do not need to invoke it with the chat_history, because it is a summarization model
    But we need to add the last message to the chat_history
    """
    # Make sure that config is populated with the session id
    if "configurable" not in config or "session_id" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}}"
        )
    
    # Get the chat history for the session
    chat_history = get_chat_history(config.get("configurable").get("session_id"))
    #print(chat_history.messages)

    messages = state['messages']

    last_message = messages[-1]

    response = model.invoke([
        HumanMessage(content=SUMMARY_LLM_PROMPT.format(context=last_message.content))
        ])
    
    chat_history.add_messages([response])

    return {"messages": response}


# # Define the function that calls the model
# def call_model(state: dict) -> str:
#     # Get the chat history for the session
#     chat_history = get_chat_history(config.get("configurable").get("session_id"))
    
#     messages = state['messages']
    
#     last_message = messages[-1]
#     prompt_input_messages = [
#         SystemMessage(content=SYSTEM_MESSAGE_PROMPT),
#         HumanMessage(content=last_message.content),
#     ]
#     response = model.invoke(prompt_input_messages)
#     return {
#         "messages": [response] # We return a list, because this will get added to the existing list
#             }

# def call_summary_model(state: dict) -> str:
    
#     messages = state['messages']
    
#     last_message = messages[-1]
    
#     prompt_input_messages = [
#         #SystemMessage(content=SYSTEM_MESSAGE_PROMPT),
#         HumanMessage(content=SUMMARY_LLM_PROMPT.format(context=last_message.content)),
#     ]
#     response = model.invoke(prompt_input_messages)
#     return {
#         "messages": [response] # We return a list, because this will get added to the existing list
#             }