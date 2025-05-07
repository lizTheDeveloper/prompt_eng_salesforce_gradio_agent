from agents import Agent, Runner
import asyncio
from agent_tools import fetch_weather

agent = Agent(
    name="Haiku Writer", 
    instructions="You are a helpful assistant that writes haikus.",
    tools=[fetch_weather]
)

async def main():
    result = await Runner.run(agent, "Write a haiku about the current weather in Tokyo")
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
