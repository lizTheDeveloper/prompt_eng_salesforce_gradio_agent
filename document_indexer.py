import numpy as np
import faiss
import os
import openai
from faiss import IndexFlatL2
from faiss import write_index



## get document embeddings from groq
import json

client = openai.OpenAI()

# Initialize list to store documents and embeddings
documents = []
document_embeddings = []

# Read documents from JSONL file
with open("research_papers.jsonl", "r") as file:
    for line in file:
        paper = json.loads(line)
        documents.append(paper["abstract"])


## get embeddings for all documents from openai
# Get embeddings for each document
for document in documents:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=document
    )
    document_embeddings.append(response.data[0].embedding)

# Convert to numpy array for FAISS
document_embeddings = np.array(document_embeddings)


# Create a FAISS index
dimension = document_embeddings.shape[1]  # Get dimension from your embeddings
index = faiss.IndexFlatL2(dimension)  # L2 distance index

# Convert embeddings to numpy float32 array if not already
embeddings_np = np.array(document_embeddings).astype(np.float32)

# Add vectors to the index
index.add(embeddings_np)

write_index(index, "document_index.dat")