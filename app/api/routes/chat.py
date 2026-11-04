from fastapi import APIRouter
from google.genai import types

from app.ai.adk import APP_NAME, runner, session_service
from app.schemas.chatSchema import ChatRequest, ChatResponse


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest):

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=request.user_id,
    )

    content = types.Content(
        role="user",
        parts=[
            types.Part(text=request.message),
        ],
    )

    response_text = ""
    tools_used = []

    async for event in runner.run_async(
        user_id=request.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content and event.content.parts:

            for part in event.content.parts:

                if part.function_call:
                    function_call = part.function_call

                    tools_used.append(
                        {
                            "name": function_call.name,
                            "arguments": dict(
                                function_call.args or {}
                            ),
                        }
                    )

        if event.is_final_response():

            if event.content and event.content.parts:

                for part in event.content.parts:

                    if part.text:
                        response_text += part.text

    return ChatResponse(
        answer=response_text,
        tools_used=tools_used,
    )