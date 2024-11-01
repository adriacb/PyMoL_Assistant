from src.models import *

import operator
from typing import TypedDict, Annotated

from langchain_core.agents import AgentAction
from langgraph.graph import add_messages, MessagesState

class AgentState(TypedDict):
    # This complex state not only tracks a count but also maintains a list of messages.
    count: int
    messages: Annotated[list, add_messages]
