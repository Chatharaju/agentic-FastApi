import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from app.core.config import get_settings

# Load application settings from .env
settings = get_settings()

# Pass the existing Gemini API key to Google ADK
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key

# Import the agent only after configuring the API key
from app.agents.business_agent import root_agent


APP_NAME = "agentic_fastapi"

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)