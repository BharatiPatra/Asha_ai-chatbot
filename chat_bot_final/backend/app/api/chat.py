from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from uuid import uuid4

from app.services.chat_service import ChatService
from app.models.chat import ChatMessage
from agent.agent_graph import agent_graph

router = APIRouter()

# Request body for sending a message
class ChatRequest(BaseModel):
    session_id: str
    content: str

# Request body for fetching chat history
class SessionRequest(BaseModel):
    session_id: str

# Response model
class ChatResponse(BaseModel):
    reply: str
    timestamp: str
    session_id: str

@router.get("/test")
async def read_test():
    return {"message": "Hello, world!"}

@router.post("/chat")
async def chat_endpoint(message_data: ChatRequest):
    print("Received message data")
    session_id = message_data.session_id.strip()
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")

    if not message_data.content:
        raise HTTPException(status_code=400, detail="Message content is required")

    chat_service = ChatService()

    timestamp = datetime.utcnow()

    # Prepare user message
    user_msg = ChatMessage(
        id=str(uuid4()),
        role="user",
        message=message_data.content,
        timestamp=timestamp
    )

    print("Session ID:", session_id)
    if session_id:
        last_5_chats = await chat_service.get_last_5_chats(session_id)
    else:
        last_5_chats = []
    print("Last 5 chats:", last_5_chats)
    state =  await agent_graph.ainvoke(

        {
            "history":last_5_chats, 
            "compiled_history":"",
            "query":message_data.content, 
            "rag_response":"", 
            "tavily_response":"",
            "response":""
        }
    )
    bot_reply = state["response"]
    

    # Prepare bot message
    bot_msg = ChatMessage(
        id=str(uuid4()),
        role="assistant",
        message=bot_reply,
        timestamp=datetime.utcnow()
    )

    # Save both messages
    await chat_service.add_messages(session_id, [user_msg, bot_msg])

    return ChatResponse(
        reply=bot_reply,
        timestamp=bot_msg.timestamp.isoformat(),
        session_id=session_id
    )

@router.post("/chat/history")
async def get_chat_history(data: SessionRequest):
    session_id = data.session_id.strip()
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")

    chat_service = ChatService()

    # 24-hour filter
    cutoff = datetime.utcnow() - timedelta(hours=24)
    messages = await chat_service.get_messages(session_id=session_id, after=cutoff)

    return {
        "messages": messages,
        "session_id": session_id
    }