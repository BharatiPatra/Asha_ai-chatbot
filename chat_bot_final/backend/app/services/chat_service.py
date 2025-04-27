from typing import List
from datetime import datetime
from fastapi import HTTPException
from app.models.chat import ChatMessage
from app.core.database import db

class ChatService:
    async def add_messages(self, session_id: str, messages: List[ChatMessage]):
        try:
            result = await db["chat_sessions"].update_one(
                {"session_id": session_id},
                {
                    "$push": {
                        "messages": {
                            "$each": [msg.dict() for msg in messages]
                        }
                    },
                    "$set": {"updated_at": datetime.utcnow()},
                    "$setOnInsert": {"created_at": datetime.utcnow()}
                },
                upsert=True
            )
            return {"status": "messages added", "count": len(messages)}
        except Exception as e:
            print(f"Error adding messages: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_messages(self, session_id: str, after: datetime = None):
        try:
            session = await db["chat_sessions"].find_one({"session_id": str(session_id)})
            if session:
                all_messages = session.get("messages", [])

                # 🕒 Filter messages if after is provided
                if after:
                    filtered_messages = [
                        msg for msg in all_messages
                        if "timestamp" in msg and msg["timestamp"] > after
                    ]
                    return filtered_messages
                return all_messages
            return []
        except Exception as e:
            print(f"Error fetching messages: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    async def get_last_5_chats(self, session_id: str):
        try:
            session = await db["chat_sessions"].find_one({"session_id": str(session_id)})
            if session:
                all_messages = session.get("messages", [])

                filtered_messages = all_messages[-5:]
                return filtered_messages
            return []
        except Exception as e:
                print(f"Error fetching messages: {e}")
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
