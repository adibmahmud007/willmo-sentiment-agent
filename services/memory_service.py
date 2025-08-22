from typing import Dict, List, Optional
from datetime import datetime
from models.memory_models import UserMemory, ConversationEntry
from config import config
from utils.helpers import is_important_conversation, clean_text
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryService:
    def __init__(self):
        # In-memory cache for user memories
        self.user_memories: Dict[str, UserMemory] = {}
    
    def get_user_memory(self, user_id: str) -> UserMemory:
        """Get or create user memory"""
        if user_id not in self.user_memories:
            self.user_memories[user_id] = UserMemory(user_id=user_id)
            logger.info(f"Created new memory for user: {user_id}")
        
        return self.user_memories[user_id]
    
    def get_memory_context(self, user_id: str) -> str:
        """Get formatted memory context for AI prompt"""
        memory = self.get_user_memory(user_id)
        
        if not memory.recent_conversations and not memory.archived_conversations:
            return "This is a new conversation with no previous context."
        
        context = "Previous conversation history:\n\n"
        
        # Add recent conversations (most important)
        if memory.recent_conversations:
            context += "Recent conversations:\n"
            for i, conv in enumerate(memory.recent_conversations[-5:], 1):  # Last 5 recent
                # Format timestamp
                time_str = conv.timestamp.strftime("%Y-%m-%d %H:%M")
                
                # Add conversation
                if conv.message_type == "voice" and conv.transcribed_text:
                    context += f"{i}. [{time_str}] User (voice): {conv.transcribed_text}\n"
                else:
                    context += f"{i}. [{time_str}] User: {conv.user_message}\n"
                
                context += f"   AI: {conv.ai_response[:200]}{'...' if len(conv.ai_response) > 200 else ''}\n\n"
        
        # Add some archived context if recent is limited
        if len(memory.recent_conversations) < 3 and memory.archived_conversations:
            context += "Earlier context:\n"
            for conv in memory.archived_conversations[-2:]:  # Last 2 archived
                time_str = conv.timestamp.strftime("%Y-%m-%d")
                if conv.message_type == "voice" and conv.transcribed_text:
                    context += f"- [{time_str}] User asked (voice): {conv.transcribed_text[:100]}...\n"
                else:
                    context += f"- [{time_str}] User asked: {conv.user_message[:100]}...\n"
        
        return context.strip()
    
    def add_conversation(
        self, 
        user_id: str, 
        user_message: str, 
        ai_response: str, 
        message_type: str = "text",
        transcribed_text: str = ""
    ) -> bool:
        """Add new conversation to user memory"""
        memory = self.get_user_memory(user_id)
        
        # Check if conversation is worth remembering (for text messages)
        if message_type == "text" and not is_important_conversation(user_message, ai_response):
            logger.info(f"Skipping trivial conversation for user: {user_id}")
            return False
        
        # For voice messages, always store (since user made effort to record)
        
        # Create conversation entry
        conversation = ConversationEntry(
            timestamp=datetime.now(),
            user_message=clean_text(user_message),
            ai_response=clean_text(ai_response),
            message_type=message_type,
            transcribed_text=clean_text(transcribed_text) if transcribed_text else ""
        )
        
        # Add to recent conversations
        memory.recent_conversations.append(conversation)
        memory.conversation_count += 1
        memory.last_updated = datetime.now()
        
        # Optimize memory if needed
        self._optimize_memory(memory)
        
        logger.info(f"Added {message_type} conversation for user: {user_id} (total: {memory.conversation_count})")
        return True
    
    def _optimize_memory(self, memory: UserMemory):
        """Optimize memory by moving old conversations to archive"""
        # If recent conversations exceed limit, move oldest to archived
        if len(memory.recent_conversations) > config.MAX_RECENT_MEMORIES:
            # Move oldest recent conversations to archived
            to_archive = memory.recent_conversations[:-config.MAX_RECENT_MEMORIES]
            memory.archived_conversations.extend(to_archive)
            memory.recent_conversations = memory.recent_conversations[-config.MAX_RECENT_MEMORIES:]
        
        # If archived conversations exceed limit, remove oldest
        if len(memory.archived_conversations) > config.MAX_ARCHIVED_MEMORIES:
            memory.archived_conversations = memory.archived_conversations[-config.MAX_ARCHIVED_MEMORIES:]
        
        logger.info(f"Memory optimized - Recent: {len(memory.recent_conversations)}, Archived: {len(memory.archived_conversations)}")
    
    def clear_user_memory(self, user_id: str) -> bool:
        """Clear all memory for a user"""
        if user_id in self.user_memories:
            del self.user_memories[user_id]
            logger.info(f"Cleared memory for user: {user_id}")
            return True
        return False
    
    def get_memory_stats(self, user_id: str) -> Dict:
        """Get memory statistics for a user"""
        memory = self.get_user_memory(user_id)
        
        # Count message types
        text_count = sum(1 for conv in memory.recent_conversations + memory.archived_conversations 
                        if conv.message_type == "text")
        voice_count = sum(1 for conv in memory.recent_conversations + memory.archived_conversations 
                         if conv.message_type == "voice")
        
        return {
            "user_id": user_id,
            "recent_conversations": len(memory.recent_conversations),
            "archived_conversations": len(memory.archived_conversations),
            "total_conversations": memory.conversation_count,
            "text_messages": text_count,
            "voice_messages": voice_count,
            "last_updated": memory.last_updated.isoformat()
        }
    
    def get_conversation_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get raw conversation history as JSON for debugging"""
        memory = self.get_user_memory(user_id)
        
        all_conversations = memory.recent_conversations + memory.archived_conversations
        all_conversations.sort(key=lambda x: x.timestamp, reverse=True)  # Most recent first
        
        return [
            {
                "timestamp": conv.timestamp.isoformat(),
                "user_message": conv.user_message,
                "ai_response": conv.ai_response,
                "message_type": conv.message_type,
                "transcribed_text": conv.transcribed_text
            }
            for conv in all_conversations[:limit]
        ]

# Initialize global memory service
memory_service = MemoryService()