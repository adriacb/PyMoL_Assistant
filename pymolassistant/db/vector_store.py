import os
import yaml
from typing import Any
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), os.pardir, ".env"))

from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
from qdrant_client.http import models


QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["QDRANT_API_KEY"] = QDRANT_API_KEY
print("Qdrant API Key: ", QDRANT_API_KEY[:5])
print("OpenAI API Key: ", OPENAI_API_KEY[:5])
print("Anthropic API Key: ", ANTHROPIC_API_KEY[:5])

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
        #print("QDRANT_URL: ", QDRANT_URL)
        #print("QDRANT_COLLECTION_NAME: ", QDRANT_COLLECTION_NAME)
        
        # Qdrant instance
        qdrant = Qdrant.from_existing_collection(
            url=QDRANT_URL,
            embedding=embeddings,
            collection_name=QDRANT_COLLECTION_NAME,
            vector_name=config.get('qdrant').get('vector_name'), 
            content_payload_key=config.get('qdrant').get('content_payload_key'),
            distance_strategy=config.get('qdrant').get('vector_config').get('distance').upper()
    )

    except Exception as e:
        # If the Qdrant client fails to initialize, create a new one with an in-memory database
        print(str(e))
        raise NotImplementedError("Failed to initialize Qdrant client.")
    
    return qdrant
