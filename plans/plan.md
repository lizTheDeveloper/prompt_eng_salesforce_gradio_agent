# Meeting Rescheduler Chatbot: Implementation Plan

**New Directive:**
- The Gradio chatbot interface will use an LLM agent (via OpenAI Agents SDK) responsible for writing the reply, choosing when to use tools, and invoking them as needed. The agent will not simply echo user messages, but will act as an intelligent assistant.

This plan breaks down the project into actionable steps, each with a checkbox for tracking progress. Each step is designed to be completed in a single chat session by a coding agent.

---

## 1. Project Setup
- [x] Create project directory structure (`/app`, `/plans`, `/requirements.txt`)
- [x] Set up and activate Python virtual environment in `./env`
- [x] Create initial `requirements.txt` with Gradio, OpenAI Agents SDK, Google API Python Client
- [x] Initialize Git repository and add `.gitignore`

## 2. Google API Integration
- [x] Set up Google Cloud project and enable Gmail & Google Calendar APIs
- [x] Create OAuth 2.0 credentials and download `credentials.json`
- [x] Implement OAuth 2.0 authentication flow in Python
- [x] Request and store user permissions for Gmail and Calendar APIs (session only)

## 3. Gradio Chatbot UI
- [x] Create a basic Gradio chatbot interface
- [x] Ensure UI is accessible (keyboard, screen reader)
- [x] Add branding: minimal, clean, professional
- [x] Integrate an LLM agent (OpenAI Agents SDK) into the Gradio interface so that the agent is responsible for writing replies and choosing/using tools, not just echoing user messages.

## 4. Calendar Functionality
- [x] Implement function to fetch all meetings for a user-specified week from Google Calendar
- [x] Classify meetings as recurring or one-off
- [x] Present meeting list in chat for user review

## 5. Meeting Management
- [x] Implement flexible cancellation of meetings via Google Calendar API (by week, day, meeting, or type)
    - Backend function allows cancellation by meeting ID, date, date range, type (recurring/one-off), or summary keywords
- [x] Log all actions and errors for troubleshooting

## 6. Email Drafting and Sending
- [x] Use OpenAI Agents SDK to draft personalized emails for one-off meetings (LLM agent will handle drafting and tool invocation)
- [x] Present draft emails in chat for user review and editing
- [ ] Send reviewed emails via Gmail API

## 7. User Experience & Notifications
- [ ] Notify user in chat when actions are completed or if errors occur
- [ ] Guide user step-by-step through the process

## 8. Security & Compliance
- [ ] Ensure all user data and tokens are handled securely (no persistent storage unless permitted)
- [ ] Review code for compliance with Google API policies

## 9. Testing & Quality Assurance
- [ ] Write unit tests for major functions
- [ ] Write integration tests for API interactions
- [ ] Conduct user acceptance testing (UAT) for chatbot flows
- [ ] Test accessibility (WCAG 2.1 AA)
- [ ] Test on latest Chrome, Firefox, Safari

## 10. Deployment
- [ ] Prepare deployment environment (cloud or local server with HTTPS)
- [ ] Document deployment process
- [ ] Release: ensure all tests pass and documentation is complete

## 11. Maintenance & Support
- [ ] Set up issue reporting (GitHub or email)
- [ ] Document maintenance schedule and support procedures

---

*Check off each box as you complete the corresponding step. Each step is designed to be implemented in a single chat session for efficient progress tracking.* 