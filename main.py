from fastapi import FastAPI, Request
from email_pydantic import Email
from claude import call_claude
import httpx
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()


slack_url = os.environ.get("SLACK_URL")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    email = Email(TextBody=body["TextBody"], From=body["From"], Subject=body["Subject"])
    ai_response = await call_claude(email.TextBody)
    print(f"AI Response: {ai_response.content[0].text}")
    async with httpx.AsyncClient() as client:
        await client.post(slack_url, json={"text": ai_response.content[0].text})
    return {"received" : True}