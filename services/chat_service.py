from datetime import datetime
from models.chat_models import ChatRequest, ChatResponse
from services.groq_service import groq_service
from services.memory_service import memory_service
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.groq_service = groq_service
        self.memory_service = memory_service
    
    async def process_chat(self, user_id: str, message: str, message_type: str = "text", transcribed_text: str = "") -> ChatResponse:
        """Process a chat request with memory integration"""
        try:
            user_id = user_id
            user_message = message
            
            logger.info(f"Processing {message_type} chat for user: {user_id}")
            
            # Step 1: Get user's memory context
            memory_context = self.memory_service.get_memory_context(user_id)
            logger.info(f"Retrieved memory context for user: {user_id}")
            
            # Step 2: Generate AI response with memory context
            ai_response = self.groq_service.generate_response(user_message, memory_context)
            
            # Step 3: Add conversation to memory
            memory_updated = self.memory_service.add_conversation(
                user_id=user_id,
                user_message=user_message,
                ai_response=ai_response,
                message_type=message_type,
                transcribed_text=transcribed_text
            )
            
            # Step 4: Create response
            response = ChatResponse(
                response=ai_response,
                user_id=user_id,
                timestamp=datetime.now(),
                memory_updated=memory_updated
            )
            
            logger.info(f"Chat processed successfully for user: {user_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            # Return error response
            return ChatResponse(
                response="I'm sorry, something went wrong. Please try again.",
                user_id=user_id,
                timestamp=datetime.now(),
                memory_updated=False
            )

# Initialize global chat service
chat_service = ChatService()