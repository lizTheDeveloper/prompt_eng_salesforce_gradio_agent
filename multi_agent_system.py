from agents import Agent, handoff, Runner
import asyncio
from agent_tools import get_invoice, refund_invoice
import os
from agents.extensions.models.litellm_model import LitellmModel
import litellm


api_key = os.getenv('GROQ_API_KEY')

billing_agent = Agent(
    name="Billing agent", 
    tools=[get_invoice],
    instructions="You are a billing agent that gets invoices for a given invoice id. Please use the get_invoice tool to get the invoice.",
    model=LitellmModel(model='groq/llama3-8b-8192', api_key=api_key)
)

refund_agent = Agent(
    name="Refund agent", 
    tools=[refund_invoice],
    #instructions="You are a refund agent that refunds invoices for a given invoice id. Please use the refund_invoice tool to refund the invoice.",
    #model=LitellmModel(model='groq/llama3-8b-8192', api_key=api_key)
)

triage_agent = Agent(
    name="Triage agent", 
    handoffs=[handoff(billing_agent, tool_name_override="angry_customer_agent"), handoff(refund_agent, tool_name_override="annoy_the_customer_agent")],
    #instructions="You are a triage agent that decides which agent to hand off to based on the user's request. Please use the handoff function to hand off to the appropriate agent.",
    #model=LitellmModel(model='groq/llama3-8b-8192', api_key=api_key)
)

async def main():
    litellm._turn_on_debug()
    result = await Runner.run(triage_agent, "WHERE is the INVOCIE for 234dsfw3")
    print(result.final_output)
    
    result = await Runner.run(triage_agent, "GIVE ME MY MONTY BAK 45345")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
