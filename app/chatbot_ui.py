import gradio as gr
import datetime
import os
from typing import List
from app.calendar_utils import fetch_and_classify_meetings_for_week
from app.google_auth import get_google_services
from agents import Agent, Runner, function_tool
import openai
import base64
from email.mime.text import MIMEText

history = []

# --- MONKEY PATCH TO REMOVE 'metadata' FIELD FROM MESSAGES ---
import agents.models.openai_responses
original_fetch_response = agents.models.openai_responses.OpenAIResponsesModel._fetch_response

async def patched_fetch_response(self, system_instructions, input, model_settings, tools, output_schema, handoffs, previous_response_id, stream=False):
    # Remove 'metadata' and 'options' from any message dicts in input
    if isinstance(input, list):
        for msg in input:
            if isinstance(msg, dict):
                msg.pop('metadata', None)
                msg.pop('options', None)
    return await original_fetch_response(self, system_instructions, input, model_settings, tools, output_schema, handoffs, previous_response_id, stream)

agents.models.openai_responses.OpenAIResponsesModel._fetch_response = patched_fetch_response

BRAND_TITLE = "Meeting Rescheduler Chatbot"
BRAND_DESCRIPTION = "A professional assistant to help you reschedule meetings when planning time off."

# --- TOOL FUNCTIONS FOR AGENT ---

@function_tool
def fetch_meetings_for_week(week_start_date: str):
    """Fetch and classify meetings for the specified week (YYYY-MM-DD)."""
    date_obj = datetime.datetime.strptime(week_start_date, "%Y-%m-%d").date()
    meetings = fetch_and_classify_meetings_for_week(date_obj)
    return meetings

@function_tool
def draft_email(to: List[str], subject: str, body: str):
    """
    Create a draft email in the user's Gmail account (does not send).
    Args:
        to: list of recipient email addresses
        subject: email subject
        body: email body (plain text)
    Returns:
        Confirmation message and draft id (or link if possible)
    """
    
    _, gmail_service = get_google_services()
    message = MIMEText(body)
    message["to"] = ", ".join(to)
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft = gmail_service.users().drafts().create(
        userId="me", body={"message": {"raw": raw}}
    ).execute()
    draft_id = draft.get("id")
    return f"Draft created in Gmail. Draft ID: {draft_id}"

# --- AGENT SETUP ---

agent = Agent(
    name="Meeting Rescheduler Agent",
    instructions=(
        "You are a helpful assistant for rescheduling meetings. "
        "You can fetch meetings and draft emails. "
        "When a user needs to notify attendees, generate a professional, friendly email and use the draft_email tool to create a draft in Gmail. "
        "Do not send emails automatically; only create drafts."
    ),
    tools=[fetch_meetings_for_week, draft_email],
    model="gpt-4o",
)

# --- GRADIO CHATBOT LOGIC ---

def gradio_to_openai_history(history):
    # History is already a list of message dicts with 'role' and 'content'
    return history.copy()

def chatbot_response(user_message, history):
    import asyncio
    # Convert Gradio history to OpenAI format and append the new user message
    openai_history = gradio_to_openai_history(history)
    openai_history.append({"role": "user", "content": user_message})
    async def run_agent():
        result = await Runner.run(agent, openai_history)
        return result.final_output
    response = asyncio.run(run_agent())
    return history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": response}
    ]


def main():
    with gr.Blocks(theme=gr.themes.Base(), title=BRAND_TITLE) as demo:
        gr.Markdown(f"# {BRAND_TITLE}\n{BRAND_DESCRIPTION}")
        chatbot = gr.Chatbot(
            label="Chat",
            show_copy_button=True,
            show_share_button=False,
            height=400,
            elem_id="chatbot",
            type="messages",
        )
        user_input = gr.Textbox(
            placeholder="Type your message and press Enter...",
            show_label=False,
            elem_id="user-input",
            autofocus=True,
        )
        clear_btn = gr.Button("Clear Chat")

        user_input.submit(chatbot_response, [user_input, chatbot], chatbot)
        clear_btn.click(lambda: [], None, chatbot)

    demo.launch(share=True)

if __name__ == "__main__":
    main()
