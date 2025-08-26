from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class ConversationEntry(BaseModel):
    timestamp: datetime
    user_message: str
    age: str  # Always store age
    ai_response: str
    message_type: str = "text"  # "text" or "voice"
    transcribed_text: str = ""  # Only for voice messages

class UserMemory(BaseModel):
    user_id: str
    recent_conversations: List[ConversationEntry] = []
    archived_conversations: List[ConversationEntry] = []
    conversation_count: int = 0
    last_updated: datetime = datetime.now()
