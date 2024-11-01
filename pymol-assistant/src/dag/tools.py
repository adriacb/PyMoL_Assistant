import os
from typing import Optional

from src.db.vector_store import *
from src.models import *

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import OpenAIEmbeddings
from langchain_core.agents import AgentAction

# Load the config file
config = load_config()

EMBEDDING_MODEL = config.get('embeddings').get('model')

# TODO: config the embedding model in the config file
# Embeddings instance
embed_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

# Qdrant instance
qdrant = load_vector_store(config=config, embeddings=embed_model)

# RAG toolkit

@tool("rag_search_pymol_docs", args_schema=RagSearchSchema)
def rag_search_pymol_docs(
    query: str, 
    top_k: Optional[int] = 4
    ) -> str:
    """
   Refere to the PyMOL documentation to find the top k results for the query.

    Args:
        query (str): The query to search the PyMOL documentation.
        top_k (int): The number of results to return.

    Returns:
        str: The top k results in the documentation.
    """
    print("Query: ", query)
    # Get the top k results for the query
    results = qdrant.similarity_search_with_score(query=query, k=top_k)
    #return results List[Tuple[Document, float]]
    context: str = f"The query: {query}\n\nTop {top_k} results in the documentation:\n"
    for doc, score in results:
        print(f"Score: {score}")
        print(f"Doc: {doc.page_content[:50]}")
        d = f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]"
        context += d + "\n"
    
    return context



# we can run the tool in the following way:
# rag_search_pymol_docs.invoke(input={
# "query": "How to load a molecule in PyMOL",
# "qdrant": qdrant,
# "top_k": 5
# }



# Define more tools here

tools = [
    rag_search_pymol_docs,
    FinalResponse
    ] # Add more tools here

# Create a tool node
tool_node = ToolNode(
    tools=tools, 
    name='tools',
    #handle_tool_errors=True
    )

