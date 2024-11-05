import os
import yaml
import pickle
import pandas as pd
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http import models as rest

from pymolassistant.db.vector_store import get_distance, load_config

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# https://cloud.qdrant.io/

config = load_config()

QDRANT_URL = config.get('qdrant').get('url')
QDRANT_COLLECTION_NAME = config.get('qdrant').get('collection_name')

if not os.path.exists('../../prep/data/pymol-docs.pkl'):
    raise FileNotFoundError("Pickle file not found in the data directory.")

# # Load the data from the parquet file
# data = pd.read_parquet(config.get('data').get("parquet_file"))

# Load the data from the pkl
with open('../../prep/data/pymol-docs.pkl', 'rb') as f:
    data = pickle.load(f)

#from dict to embedding
data['vector_name'] = data['vector_name'].apply(lambda x: x['embedding'])
data['vector_content'] = data['vector_content'].apply(lambda x: x['embedding'])


# This initializes the Qdrant client 
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# This creates a collection in Qdrant
vectors_config = models.VectorParams(
    size=config.get('qdrant').get('vector_config').get('size'),                             # Size of the vector 
    distance=get_distance(config.get('qdrant').get('vector_config').get('distance').lower())       # Distance metric
    )

# # Create a collection in Qdrant
# qdrant_client.create_collection(
#     QDRANT_COLLECTION_NAME,
#     vectors_config
#     )

qdrant_client.recreate_collection(
    collection_name=QDRANT_COLLECTION_NAME,
    vectors_config={
        "name": rest.VectorParams(
            size=len(data['vector_name'].iloc[0]),
            distance=get_distance(config.get('qdrant').get('vector_config').get('distance').lower())
        ),
        "content": rest.VectorParams(
            size=len(data['vector_content'].iloc[0]),
            distance=get_distance(config.get('qdrant').get('vector_config').get('distance').lower())
        )
    }
)

# This inserts the vectors into the collection
qdrant_client.upsert(
    collection_name=QDRANT_COLLECTION_NAME,
    points=[
        models.PointStruct(                  # This is the vector
            id=k,
            vector={
                "name": v['vector_name'],
                "content": v['vector_content']
            },
            payload=v.to_dict(),           # This is the metadata
        )
        for k, v in data.iterrows()        # Iterate over the rows of the dataframe
    ],
)

# https://cloud.qdrant.io/