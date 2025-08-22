from fastapi import APIRouter
from datetime import datetime

# Create router for health/system endpoints
router = APIRouter(tags=["Health"])

@router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Willmo Chat - Voice & Text Chatbot API with JSON Memory",
        "status": "running",
        "version": "2.0.0",
        "features": ["text_chat", "voice_chat", "json_memory", "conversation_history"]
    }

@router.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "willmo-chat",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "groq_api": "connected",
            "memory_service": "active",
            "transcription_service": "active"
        }
    }