from fastapi import FastAPI, Request
from email_pydantic import Email
from claude import call_claude
import requests
import httpx
import os
from dotenv import load_dotenv

app = FastAPI()

slack_url = os.environ.get("SLACK_URL")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    email = Email(TextBody=body["TextBody"], From=body["From"], Subject=body["Subject"])
    # print(f"Received webhook: {body['TextBody']}")
    # print(f"Subject: {email.Subject}, From: {email.From}, TextBody: {email.TextBody}")
    ai_response = await call_claude(email.TextBody)
    print(f"AI Response: {ai_response}")
    return {"received" : True}