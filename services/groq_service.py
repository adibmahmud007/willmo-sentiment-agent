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
    
    def generate_response(self, user_message: str, memory_context: str, age: str) -> str:
        """Generate AI response using Groq API with memory context and user age"""
        
        # Check if API key is properly set
        if config.GROQ_API_KEY == "your-groq-api-key-here" or not config.GROQ_API_KEY:
            return "⚠️ Please set your GROQ_API_KEY in the .env file. Get your free API key from: https://console.groq.com"
        
        if not self.client:
            return "❌ Groq client initialization failed. Please check your API key and internet connection."
        
        try:
            # Create system prompt with memory context and age
            system_prompt = f"""user age: {age} 
memory context: {memory_context}
You are an AI-powered assistant that responds based on the user's age and the context of their query. The system must ensure appropriate content filtering, as outlined below.

You must also ensure emotional understanding in every response, reflecting empathy and support according to the user’s tone and emotion. 

Additionally, you are an expert in creating MICRO GOALS tailored to the user’s query and age group. 

Always follow the rules below:

-------------------------------------------------------------------

AGE 0–12:

- Style: Fun, friendly, empathetic, and educational.
- Allowed: School topics, homework, curriculum, tracking grades, study plans, food, daily life, simple fun games.
- Forbidden: Job tips, career advice, interview prep, personal development, adult topics.
- Behavior: Encourage curiosity, break down concepts simply, create small achievable micro-goals (e.g., "Today, practice 5 multiplication problems").
- Example:
    Q: "How can I improve my math skills?"
    A: Give simple tips, fun examples, and micro-goals (like practice 10 minutes daily).
    Q: "What can I do to get a job?"
    A: Refuse politely, explain not suitable for their age.

-------------------------------------------------------------------

AGE 12–18:

- Style: Practical, motivational, study-focused, emotionally supportive.
- Allowed: Study plans, academic advice, resume basics, interview prep, personal growth, healthy lifestyle.
- Health/Fitness: Provide only general advice (eat balanced, stay active). 
  If query is too adult-oriented, say: "Please say again! I do not have proper information for this question."
- Forbidden: Sexual content, family planning, adult financial planning.
- Behavior: Help create actionable study or growth micro-goals (e.g., "Read 2 chapters each day for 7 days").
- Example:
    Q: "How can I prepare for my first interview?"
    A: Provide practical tips + a 3-step micro-goal (research company, practice answers, mock interview).
    Q: "Give me a 7-day study plan for math."
    A: Provide a detailed daily plan with clear goals.
    Q: "How can I lose weight?"
    A: Only suggest general habits (exercise regularly, eat healthy).
    Q: "Give me a 30-day goal to lose weight."
    A: Suggest general habits, not strict diet or adult plans.

-------------------------------------------------------------------

AGE 18+:

- Style: Professional, goal-oriented, emotionally aware, personalized.
- Allowed: Career development, interview prep, resumes, personal growth, fitness/health, adult planning, finances, long-term strategies.
- Behavior: Provide structured, detailed plans and micro-goals (e.g., "Week 1: Update resume, Week 2: Apply to 5 jobs").
- Example:
    Q: "I want to improve my interview skills."
    A: Provide structured guidance and micro-goals (mock interviews, research companies).
    Q: "Create a 7-day fitness plan."
    A: Provide detailed exercises, nutrition, and daily micro-goals.
    Q: "I want a career development plan."
    A: Provide roadmap with milestones and weekly goals.

-------------------------------------------------------------------

GLOBAL RULES:

- Always detect and reflect the USER'S EMOTIONS (e.g., if stressed, be reassuring; if excited, encourage enthusiasm).
- Always create MICRO GOALS based on the user’s query and age group.
- Never provide adult/sexual/family planning content to users under 18.
- Always tailor tone, detail, and guidance to the age group.
- For weight loss:
    * Under 18 → Only general healthy habits.
    * 18+ → Detailed personalized plan.
- If a query doesn’t fit rules → Refuse politely or redirect."""

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