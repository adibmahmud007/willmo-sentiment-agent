from groq import Groq
from config import config
import logging
import tempfile
import os
from typing import Optional

logger = logging.getLogger(__name__)

class AudioTranscriptionService:
    def __init__(self):
        try:
            self.client = Groq(api_key=config.GROQ_API_KEY)
            self.model = "whisper-large-v3"  # Groq's Whisper model
            logger.info("Audio transcription service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize audio transcription service: {str(e)}")
            self.client = None
    
    def transcribe_audio(self, audio_file_content: bytes, filename: str) -> Optional[str]:
        """
        Transcribe audio file content to text using Groq Whisper API
        
        Args:
            audio_file_content: Raw audio file bytes
            filename: Original filename for format detection
            
        Returns:
            Transcribed text or None if failed
        """
        
        # Check if API key is properly set
        if config.GROQ_API_KEY == "your-groq-api-key-here" or not config.GROQ_API_KEY:
            logger.error("Groq API key not properly configured")
            return "⚠️ Please set your GROQ_API_KEY in the .env file."
        
        if not self.client:
            logger.error("Groq client not initialized")
            return "❌ Audio transcription service not available."
        
        # Validate file format
        supported_formats = ['.mp3', '.wav', '.m4a', '.mp4', '.mpeg', '.mpga', '.webm']
        file_extension = os.path.splitext(filename.lower())[1]
        
        if file_extension not in supported_formats:
            return f"❌ Unsupported audio format. Supported formats: {', '.join(supported_formats)}"
        
        try:
            # Create temporary file for Groq API
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                temp_file.write(audio_file_content)
                temp_file_path = temp_file.name
            
            try:
                # Transcribe using Groq Whisper API
                with open(temp_file_path, "rb") as audio_file:
                    transcription = self.client.audio.transcriptions.create(
                        file=(filename, audio_file, "audio/mpeg"),
                        model=self.model,
                        prompt="",  # Optional context
                        response_format="text",  # Get plain text
                        language="en",  # Auto-detect if not specified
                        temperature=0.0  # More deterministic
                    )
                
                # Clean up temporary file
                os.unlink(temp_file_path)
                
                if isinstance(transcription, str):
                    transcript_text = transcription.strip()
                else:
                    # Handle if response is an object with text attribute
                    transcript_text = getattr(transcription, 'text', str(transcription)).strip()
                
                if not transcript_text:
                    return "❌ No speech detected in the audio file."
                
                logger.info(f"Successfully transcribed audio: {len(transcript_text)} characters")
                return transcript_text
                
            except Exception as e:
                # Clean up temporary file in case of error
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                raise e
                
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            
            if "authentication" in str(e).lower() or "api_key" in str(e).lower():
                return "🔑 Authentication failed. Please check your GROQ_API_KEY."
            elif "rate_limit" in str(e).lower():
                return "⏳ Rate limit reached. Please try again in a moment."
            elif "file" in str(e).lower() and "size" in str(e).lower():
                return "📁 Audio file too large. Please use a smaller file (max 25MB)."
            else:
                return f"❌ Transcription failed: {str(e)}"
    
    def validate_audio_file(self, file_content: bytes, filename: str) -> tuple[bool, str]:
        """
        Validate if the uploaded file is a valid audio file
        
        Returns:
            (is_valid, error_message)
        """
        # Check file size (Groq limit is 25MB)
        max_size = 25 * 1024 * 1024  # 25MB in bytes
        if len(file_content) > max_size:
            return False, "File too large. Maximum size is 25MB."
        
        if len(file_content) == 0:
            return False, "Empty file uploaded."
        
        # Check file extension
        supported_formats = ['.mp3', '.wav', '.m4a', '.mp4', '.mpeg', '.mpga', '.webm']
        file_extension = os.path.splitext(filename.lower())[1]
        
        if file_extension not in supported_formats:
            return False, f"Unsupported format. Supported: {', '.join(supported_formats)}"
        
        return True, "Valid audio file"

# Initialize global transcription service
transcription_service = AudioTranscriptionService()