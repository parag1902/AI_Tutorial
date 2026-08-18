#Imports

import os
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_clinet.models import Distance, VectorParams, PointStruct


#Loading enviorment variables from .env

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
QDRANT_URL=os.getenv("QDRANT_URL")

if not GROQ_API_KEY or QDRANT_API_KEY or QDRANT_URL:
    print("Check your GROQ or QDRANT api key or URL")

#Connecting with GROQ and QDRANT

llm_client=Groq(api_key=GROQ_API_KEY)
print("LLM Connected Successfully")
db_client=QdrantClient(api_key=QDRANT_API_KEY, url=QDRANT_URL)
print("DB Connected Successfully")

########Creating Qdrant Collection###########

collection_name="knowledge"
embedding_size=384

#First Deleting exixsting collection if exists

if db_client.collection_exists(collection_name):
    print(f"Deleting the existing collection = {collection_name}")
    db_client.delete_collection(collection_name)

#Creating the Collection
db_client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(
        size=embedding_size,
        distance=Distance.Cosine,
    ),
)

print(f"{collection_name} is created with vector size of {embedding_size}")
print("Distance: Cosine")


