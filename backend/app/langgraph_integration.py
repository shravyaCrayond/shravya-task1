import asyncio
from typing import AsyncGenerator
from google import genai
from .core.config import settings
import json

client = genai.Client(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = """You are a helpful AI assistant.
Instructions for generating responses:
- Provide clear, structured, and actionable advice.
- Remember previous queries of user for continuous chat.
- Avoid generic responses; alter according to user's input.
- Format output using markdown:
  - Use **bold** for highlights.
  - Use *italic* where you want users to remember.
  - Use subheadings (###) for sections.
  - Use bullet points (-) for lists.
  - Use line breaks (\\n) to separate sections clearly.
- Highlight as links where "https://" is observed.
"""

async def generate_stream(prompt: str) -> AsyncGenerator[str, None]:
    """
    Sequentially yields text chunks from Gemini in proper order.
    """
    final_prompt = SYSTEM_PROMPT + "\nUser: " + prompt

    for part in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=[final_prompt]
    ):
        text = getattr(part, "text", None) or getattr(part, "delta", None)
        if text:
            yield text
        await asyncio.sleep(0)

async def event_stream(prompt: str) -> AsyncGenerator[str, None]:
    """
    Formats Gemini chunks as SSE events for StreamingResponse.
    """
    async for chunk in generate_stream(prompt):
        yield f"data: {json.dumps({'text': chunk})}\n\n"
