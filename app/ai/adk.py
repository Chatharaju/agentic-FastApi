from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from app.agents.business_agent import root_agent


APP_NAME = 'agentic_fastapi'
session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)