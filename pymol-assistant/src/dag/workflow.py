import os

from src.dag.tools import tool_node
from src.dag.nodes import call_model, should_continue, call_summary_model

from langgraph.graph import MessagesState, START, StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


# Define a new graph
workflow = StateGraph(
    # Define the initial state of the graph
    state_schema=MessagesState
)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("summary_agent", call_summary_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.add_edge(START, "agent")

# Add a conditional edge from `agent` to `tools`
workflow.add_conditional_edges(
    "agent", 
    should_continue, 
    ["tools", "summary_agent", END]
    )

# We now add a normal edge from `tools` to `summary_agent`.
# This means that after `tools` is called, `summary_agent` node is called next.
workflow.add_edge("tools", 'summary_agent')
#workflow.add_edge("summary_agent", END)


# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Note that we're (optionally) passing the memory when compiling the graph
graph = workflow.compile(checkpointer=checkpointer)

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
