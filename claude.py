import anthropic
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

client = anthropic.AsyncAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

async def call_claude(email):
    message = await client.messages.create(
                    model="claude-opus-4-7",
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": f"Summarise this email for me in less than a paragraph. Include all the necessary details.{email}",
                        }
                    ],
                )
    
    return message