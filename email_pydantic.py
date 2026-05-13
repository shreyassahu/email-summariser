from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Email(BaseModel, ):
    From: str
    Subject: str
    TextBody: str