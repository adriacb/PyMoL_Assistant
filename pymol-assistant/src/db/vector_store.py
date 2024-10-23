import os
import yaml
from typing import Any
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), os.pardir, ".env"))

from qdrant_client import QdrantClient
from qdrant_client.http import models

from langchain.vectorstores import Qdrant

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("Qdrant API Key: ", QDRANT_API_KEY[:5])
print("OpenAI API Key: ", OPENAI_API_KEY[:5])

def load_config(path: str = os.path.join(os.path.dirname(__file__), "config.yaml")) -> dict:
    """
    Load the config file.
    """
    try:
        config = yaml.safe_load(open(path))
        return config
    except FileNotFoundError:
        raise FileNotFoundError("Config file not found.")

def get_distance(dtype:str) -> models.Distance:
    """
    Get the distance metric from the config file.

    Args:
        dtype (str): The distance metric.

    Returns:
        models.Distance: The distance metric.
    """
    if dtype == "euclidean":
        return models.Distance.EUCLIDEAN
    elif dtype == "cosine":
        return models.Distance.COSINE
    else:
        raise ValueError(f"Invalid distance metric: {dtype}")


def load_vector_store(config:dict, embeddings:Any) -> Qdrant:
    """
    Load the vector store from the config file.
    """

    if not embeddings:
        raise ValueError("Please provide input embeddings.")

    try:
        QDRANT_URL = config.get('qdrant').get('url')
        QDRANT_COLLECTION_NAME = config.get('qdrant').get('collection_name')
        
        # This initializes the Qdrant client using the QDRANT_URL and QDRANT_API_KEY
        qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
    except Exception as e:
        # If the Qdrant client fails to initialize, create a new one with an in-memory database
        print(str(e))
        qdrant_client = QdrantClient(":memory:")

    vector_store = Qdrant(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME,
        embeddings=embeddings,
    )

    return vector_store