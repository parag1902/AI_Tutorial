#Imports

import os
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


#Loading enviorment variables from .env

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
QDRANT_URL=os.getenv("QDRANT_URL")

if not GROQ_API_KEY or not QDRANT_API_KEY or not QDRANT_URL:
    raise ValueError("Check your GROQ or QDRANT API key or URL")

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
        distance=Distance.COSINE,
    ),
)

print(f"{collection_name} is created with vector size of {embedding_size}")
print("Distance: Cosine")

#Loading Our Knowledge

with open("knowledge.txt", "r", encoding="utf-8") as f:
    documents = [
        line.strip()
        for line in f
        if line.strip()
    ]

print(f"Loaded {len(documents)} documents")

#Creating Embeddings
print("Loading embedding model")

model = SentenceTransformer("all-MiniLM-L6-v2") #384

print("Embedding model ready!")


embeddings = model.encode(documents)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")

#Creating Qdrant Points

points = []

for i, embedding in enumerate(embeddings):

    point = PointStruct(
        id=i + 1, #id=1

        vector=embedding.tolist(),

        payload={
            "text": documents[i]
        }
    )
    points.append(point)

#Uploading on Qdrant
db_client.upsert( #upload+insert
    collection_name=collection_name,
    points=points
)

print(f"Uploaded {len(points)} documents to Qdrant!")

#Search Qdrant
def search(query, top_k=3):

    # Convert the question into an embedding
    query_vector = model.encode(query).tolist()

    # Search Qdrant for similar vectors
    results = db_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points

    return results

#Test Seach
query = "How many vacation days do I get?"

results = search(query, top_k=3)

print("\nSearch results:")

for result in results:
    print(f"Score: {result.score:.3f}")
    print(result.payload["text"])
    print()

#Asking the LLM
def ask_llm(question, context):

    prompt = f"""
Answer the question using only the information provided below.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say:
"I don't know based on the provided information."
"""

    response = llm_client.chat.completions.create(
        model= "openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
question = "How many vacation days do I get?"

results = search(question, top_k=3)


# Extract text from the search results
context = "\n".join(
    result.payload["text"]
    for result in results
)


answer = ask_llm(question, context)


print("\nFinal Answer:")
print(answer)

#Complete RAg
question = "How many vacation days do I get?"

results = search(question, top_k=3)


# Extract text from the search results
context = "\n".join(
    result.payload["text"]
    for result in results
)


answer = ask_llm(question, context)


print("\nFinal Answer:")
print(answer)