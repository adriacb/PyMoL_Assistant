import os
from typing import Optional
from src.db.vector_store import load_config, load_vector_store, OPENAI_API_KEY, QDRANT_API_KEY

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import OpenAIEmbeddings

# Load the config file
config = load_config()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["QDRANT_API_KEY"] = QDRANT_API_KEY
EMBEDDING_MODEL = config.get('embeddings').get('model')

# TODO: config the embedding model in the config file
# Embeddings instance
embed_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

# Qdrant instance
qdrant = load_vector_store(config=config, embeddings=embed_model)


# RAG toolkit
@tool("rag_search_pymol_docs")
def rag_search_pymol_docs(query: str, top_k: Optional[int] = 4) -> str:
    """
    Query the PyMOL documentation using Qdrant

    Args:
        query (str): The full query to search for.
        top_k (int, optional): The number of results to return. Defaults to 4.
    
    Returns:
        str: The query and the top k results.
    """
    # Get the top k results for the query
    results = qdrant.similarity_search_with_score(query=query, k=top_k)
    
    context: str = f"The query: {query}\n\nTop {top_k} results in the documentation:\n"
    print(context)
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
    ] # Add more tools here

# Create a tool node
tool_node = ToolNode(tools=tools, name='tools')

