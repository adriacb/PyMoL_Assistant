import os

from fastapi import FastAPI

from src.logger import Logger
from src.models import QuestionModel
from src.prompts import *
from src.db.vector_store import load_config, load_vector_store, OPENAI_API_KEY, QDRANT_API_KEY

from langchain_openai import ChatOpenAI
from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.schema import (
    SystemMessage,    # Generic system message
    HumanMessage,     # HumanMessage is a message from the human
    AIMessage,        # AIMessage is a message from the AI
)

# Load the config file
config = load_config()
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["QDRANT_API_KEY"] = QDRANT_API_KEY
EMBEDDING_MODEL = config.get('embeddings').get('model')

# TODO: config logger output directory in the config file
logger = Logger(os.path.join(os.path.dirname(__file__), "logs/pymol-assistant-server.log"))
# FastAPI app instance
app = FastAPI()

# TODO: config llm model in the config file
# OpenAI chat instance
chat = ChatOpenAI(
    model='gpt-4o-mini'
)

# TODO: config the embedding model in the config file
# Embeddings instance
embed_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

# Qdrant instance
qdrant = load_vector_store(config=config, embeddings=embed_model)

# The history of the conversation
history: list = [
    SystemMessage(content=SYSTEM_MESSAGE_PROMPT),
]


def gennerate_query_to_function_prompt(
        query: str,
        qdrant: Qdrant, top_k:int=5) -> HumanMessage:
    """
    Generate a prompt for the user to provide a function and parameters for a given query.

    Args:
        query (str): The query to generate the prompt for.
        qdrant (Qdrant): The Qdrant instance.
        top_k (int): The number of top results to return.

    Returns:
        HumanMessage: The generated prompt.
    """
    # Get the top k results for the query
    results = qdrant.similarity_search(query=query, k=top_k)

    # the context will be the content of each document
    context = ""

    for i, result in enumerate(results):
        context += f"{i+1}. Document:\n{result.page_content}\n\n"

    prompt = HumanMessage(content=LLM_RAG_PROMPT.format(
        query=query,
        context=context
    ))

    return prompt



@app.post("/question")
async def submit_question(question: QuestionModel) -> dict:
    """
    Asyncronously, get the question from the client and return the response.

    Args:
        question (QuestionModel): The question from the client.
    
    Returns:
        json: The response to the question.
    """
        # Process the received question
    logger.info(f"Received question: {question.question}")
    
    # The question is transformed to HumanMessage
    response_given_query = gennerate_query_to_function_prompt(
        query=question.question,
        qdrant=qdrant,
        top_k=5
    )

    # The prompt is added to the history
    history.append(response_given_query)

    # result 
    result = await chat.invoke(history)

    # The result is added to the history
    history.append(result)

    return {"message": result.content}