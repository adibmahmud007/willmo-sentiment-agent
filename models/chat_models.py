from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    user_id: str
    message: str
    age: str
class ChatResponse(BaseModel):
    response: str
    user_id: str
    timestamp: datetime
    memory_updated: bool

class VoiceChatResponse(BaseModel):
    transcribed_text: str
    ai_response: str
    user_id: str
    timestamp: datetime
    memory_updated: bool
    transcription_success: bool

class MemoryResponse(BaseModel):
    user_id: str
    recent_conversations: List[Dict[str, Any]]
    archived_conversations: List[Dict[str, Any]]
    total_conversations: int
    text_messages: int
    voice_messages: int
    last_updated: datetime

class ConversationHistoryResponse(BaseModel):
    user_id: str
    conversations: List[Dict[str, Any]]
    total_count: int