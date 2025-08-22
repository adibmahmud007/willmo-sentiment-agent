from fastapi import APIRouter, HTTPException
from models.chat_models import MemoryResponse, ConversationHistoryResponse
from services.memory_service import memory_service
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Create router for memory-related endpoints
router = APIRouter(prefix="/api", tags=["Memory"])

@router.get("/memory/{user_id}", response_model=MemoryResponse)
async def get_user_memory(user_id: str):
    """
    Get user's memory information with JSON conversation data
    
    - **user_id**: User identifier
    
    Returns user's recent and archived conversations in JSON format
    """
    try:
        memory = memory_service.get_user_memory(user_id)
        stats = memory_service.get_memory_stats(user_id)
        
        # Convert conversations to JSON format
        recent_json = [
            {
                "timestamp": conv.timestamp.isoformat(),
                "user_message": conv.user_message,
                "ai_response": conv.ai_response,
                "message_type": conv.message_type,
                "transcribed_text": conv.transcribed_text
            }
            for conv in memory.recent_conversations
        ]
        
        archived_json = [
            {
                "timestamp": conv.timestamp.isoformat(),
                "user_message": conv.user_message,
                "ai_response": conv.ai_response,
                "message_type": conv.message_type,
                "transcribed_text": conv.transcribed_text
            }
            for conv in memory.archived_conversations
        ]
        
        return MemoryResponse(
            user_id=user_id,
            recent_conversations=recent_json,
            archived_conversations=archived_json,
            total_conversations=stats["total_conversations"],
            text_messages=stats["text_messages"],
            voice_messages=stats["voice_messages"],
            last_updated=memory.last_updated
        )
        
    except Exception as e:
        logger.error(f"Error retrieving memory for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving user memory")

@router.get("/conversations/{user_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(user_id: str, limit: int = 50):
    """
    Get complete conversation history for a user
    
    - **user_id**: User identifier
    - **limit**: Maximum number of conversations to return (default: 50)
    
    Returns complete conversation history in chronological order
    """
    try:
        conversations = memory_service.get_conversation_history(user_id, limit)
        
        return ConversationHistoryResponse(
            user_id=user_id,
            conversations=conversations,
            total_count=len(conversations)
        )
        
    except Exception as e:
        logger.error(f"Error retrieving conversation history for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving conversation history")

@router.delete("/memory/{user_id}")
async def clear_user_memory(user_id: str):
    """
    Clear all memory for a specific user
    
    - **user_id**: User identifier
    
    Returns success status
    """
    try:
        success = memory_service.clear_user_memory(user_id)
        
        if success:
            return {"message": f"Memory cleared for user: {user_id}", "success": True}
        else:
            return {"message": f"No memory found for user: {user_id}", "success": False}
        
    except Exception as e:
        logger.error(f"Error clearing memory for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error clearing user memory")

@router.get("/stats/{user_id}")
async def get_memory_stats(user_id: str):
    """
    Get memory statistics for a user
    
    - **user_id**: User identifier
    
    Returns detailed memory statistics including message type breakdown
    """
    try:
        stats = memory_service.get_memory_stats(user_id)
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")