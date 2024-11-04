import os

from src.dag.tools import *
from src.dag.nodes import *

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

########## Graph ##########
# Define a new graph
workflow = StateGraph(
    # Define the initial state of the graph
    state_schema=AgentState
    )

workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("respond", respond)
workflow.add_node("tools", call_tools)

# __start__
workflow.set_entry_point("agent")
# conditional nodes
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",        # If the condition is met, go to the "tools" node
        "end": "respond",
    }
)

workflow.add_edge("tools", "agent")
workflow.add_edge("respond", END)


# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

########## Compile and Save Graph ##########
# Note that we're (optionally) passing the memory when compiling the graph
graph = workflow.compile(
    checkpointer=checkpointer
    )

try:
    # Retrieve the PNG data of the graph
    png_data = graph.get_graph().draw_mermaid_png()
    path = os.path.join(os.path.dirname(__file__), "images/workflow.png")
    # Write the binary data to a PNG file
    with open(path, "wb") as f:
        f.write(png_data)
        
    print(f"Graph saved as '{path}'")
except Exception as e:
    print(e)

# Agents with Structured Output: https://www.youtube.com/watch?v=0i9NzY_b3pg