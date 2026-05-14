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
    try:
        body = await request.json()
        email = Email(TextBody=body["TextBody"], From=body["From"], Subject=body["Subject"])
    except Exception as e:
        print(f"Failed to parse email: {e}")
        return {"error": "Invalid email payload"}, 400
    
    try:
        ai_response = await call_claude(email.TextBody)
        summary = ai_response.content[0].text
    except Exception as e:
        print(f"Claude API failed: {e}")
        summary = f"Could not summarize. Original from {email.From}: {email.Subject}"

    try:
        async with httpx.AsyncClient() as client:
            await client.post(slack_url, json={"text": summary})
    except Exception as e:
        print(f"Slack delivery failed: {e}")
        return {"error": "Slack delivery failed"}, 500 

    return {"received": True}
    