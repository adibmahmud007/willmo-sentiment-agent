# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
    GROQ_MODEL = "llama3-8b-8192"  # Free model on Groq
    MAX_RECENT_MEMORIES = 5  # Maximum recent summaries to keep active
    MAX_ARCHIVED_MEMORIES = 10  # Maximum archived summaries to keep
    MEMORY_SUMMARY_THRESHOLD = 3  # Summarize after every 3 conversations

config = Config()