from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime

class ChatMessage(BaseModel):
    id:str
    role: str
    message: str
    timestamp: Optional[datetime] = None

class ChatMessageList(BaseModel):
    messages: List[ChatMessage]
