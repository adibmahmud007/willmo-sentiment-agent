from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from models.chat_models import ChatRequest, ChatResponse, VoiceChatResponse
from services.chat_service import chat_service
from utils.transcript_audio import transcription_service
import logging
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

# Create router for chat-related endpoints
router = APIRouter(prefix="/api", tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str =Form(...),
    message: str =Form(...)
):
    """
    Text-based chat endpoint
    
    - **user_id**: Unique identifier for the user
    - **message**: User's message to the chatbot
    
    Returns AI response with JSON memory integration
    """
    try:
        logger.info(f"Text chat request from user: {user_id}")
        
        if not user_id or not message.strip():
            raise HTTPException(
                status_code=400, 
                detail="user_id and message are required"
            )
        
        response = await chat_service.process_chat(user_id, message, message_type="text")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/voice-chat", response_model=VoiceChatResponse)
async def voice_chat_endpoint(
    user_id: str = Form(...),
    audio_file: UploadFile = File(...)
):
    """
    Voice-based chat endpoint
    
    - **user_id**: Unique identifier for the user
    - **audio_file**: Audio file (mp3, wav, m4a, etc.) containing user's voice message
    
    Process: Audio → Speech-to-Text → AI Response → JSON Memory Storage
    """
    try:
        logger.info(f"Voice chat request from user: {user_id}")
        
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        if not audio_file:
            raise HTTPException(status_code=400, detail="audio_file is required")
        
        # Read audio file content
        audio_content = await audio_file.read()
        
        # Validate audio file
        is_valid, validation_message = transcription_service.validate_audio_file(
            audio_content, audio_file.filename
        )
        
        if not is_valid:
            raise HTTPException(status_code=400, detail=validation_message)
        
        logger.info(f"Processing audio file: {audio_file.filename} ({len(audio_content)} bytes)")
        
        # Transcribe audio to text
        transcribed_text = transcription_service.transcribe_audio(
            audio_content, audio_file.filename
        )
        
        if not transcribed_text or transcribed_text.startswith(("⚠️", "❌", "🔑", "⏳", "📁")):
            # Transcription failed
            return VoiceChatResponse(
                transcribed_text=transcribed_text or "Transcription failed",
                ai_response="I couldn't understand the audio. Please try again with a clearer recording.",
                user_id=user_id,
                timestamp=datetime.now(),
                memory_updated=False,
                transcription_success=False
            )
        
        logger.info(f"Successfully transcribed: {transcribed_text[:100]}...")
        
        # Create chat request with transcribed text
        chat_request = ChatRequest(user_id=user_id, message=transcribed_text)
        
        # Process chat with AI (voice type with transcription)
        chat_response = await chat_service.process_chat(
            chat_request, 
            message_type="voice", 
            transcribed_text=transcribed_text
        )
        
        # Return voice chat response
        return VoiceChatResponse(
            transcribed_text=transcribed_text,
            ai_response=chat_response.response,
            user_id=user_id,
            timestamp=datetime.now(),
            memory_updated=chat_response.memory_updated,
            transcription_success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in voice chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Voice chat processing failed: {str(e)}")