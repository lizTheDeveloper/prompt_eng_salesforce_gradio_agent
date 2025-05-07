import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes for Gmail and Calendar APIs
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
]

def get_google_services():
    """
    Runs OAuth 2.0 flow and returns authorized Gmail and Calendar service clients.
    Tokens are persisted in token.json for testing purposes.
    """
    creds = None
    token_path = 'token.json'
    # Load credentials if they exist
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If no valid creds, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    calendar_service = build('calendar', 'v3', credentials=creds)
    gmail_service = build('gmail', 'v1', credentials=creds)
    return calendar_service, gmail_service 