from groq import Groq
from config import config
import logging

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        try:
            self.client = Groq(api_key=config.GROQ_API_KEY)
            self.model = config.GROQ_MODEL
            logger.info("Groq client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")
            # Create a dummy client for development
            self.client = None
            self.model = config.GROQ_MODEL
    
    def generate_response(self, user_message: str, memory_context: str) -> str:
        """Generate AI response using Groq API with memory context"""
        
        # Check if API key is properly set
        if config.GROQ_API_KEY == "your-groq-api-key-here" or not config.GROQ_API_KEY:
            return "⚠️ Please set your GROQ_API_KEY in the .env file. Get your free API key from: https://console.groq.com"
        
        if not self.client:
            return "❌ Groq client initialization failed. Please check your API key and internet connection."
        
        try:
            # Create system prompt with memory context and get the latest memory context
            system_prompt = f"""You are a helpful AI assistant with memory of previous conversations.

{memory_context}

Instructions:
- Use the conversation context to provide personalized responses
- Remember user preferences and past topics
- Be natural and conversational
- If no previous context, introduce yourself briefly
- Keep responses concise but helpful
- Understand the user's intent and provide a helpful response
- Understand users sentiment and give a empathetic response
- if user is adult and you know that the user is asking for sexual content then give a response in romantic way but dont go deeper. and you dont need to say anything like youre respected agent or something like that"""

            # Generate response by ai 
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model=self.model,
                max_tokens=500,
                temperature=0.7,
                top_p=1,
                stream=False
            )
            
            response = chat_completion.choices[0].message.content
            logger.info(f"Generated response with Groq API (model: {self.model})")
            
            return response
        
        except Exception as e:
            logger.error(f"Error generating response with Groq: {str(e)}")
            if "authentication" in str(e).lower() or "api_key" in str(e).lower():
                return "🔑 Authentication failed. Please check your GROQ_API_KEY in the .env file."
            elif "rate_limit" in str(e).lower():
                return "⏳ Rate limit reached. Please try again in a moment."
            else:
                return f"❌ I'm having trouble processing your request: {str(e)}"

# Initialize global Groq service
groq_service = GroqService()