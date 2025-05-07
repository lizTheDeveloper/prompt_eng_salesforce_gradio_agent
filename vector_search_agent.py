from agents import Agent, Runner, function_tool
import asyncio
import openai
from faiss import read_index
import numpy as np
client = openai.OpenAI()

index = read_index("document_index.dat")

@function_tool
def vector_search(query: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = response.data[0].embedding
    ## numpy array
    query_embedding = np.array([query_embedding])
    Document, Index_of_document = index.search(query_embedding, k=10)
    return Document, Index_of_document

agent = Agent(
    name="Paper Query Guy", 
    instructions="You are a helpful assistant that finds papers based on a query.",
    tools=[vector_search]
)

async def main():
    result = await Runner.run(agent, "Anything about robotic welding in there? Explain what you find. What's the index of the document?")
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())