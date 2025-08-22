# utils/helpers.py
import json
from datetime import datetime
from typing import Dict, Any

def is_important_conversation(message: str, response: str) -> bool:
    """
    Determine if a conversation contains important information worth summarizing
    """
    # Simple heuristics - can be improved with ML
    trivial_patterns = [
        "hi", "hello", "bye", "thanks", "ok", "yes", "no",
        "how are you", "what's up", "good morning", "good night"
    ]
    
    message_lower = message.lower().strip()
    
    # If message is very short and matches trivial patterns
    if len(message_lower) < 20 and any(pattern in message_lower for pattern in trivial_patterns):
        return False
    
    # If conversation has substantial content
    if len(message) > 50 or len(response) > 100:
        return True
    
    return True

def format_timestamp() -> str:
    """Format current timestamp for logging"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def clean_text(text: str) -> str:
    """Clean and format text for memory storage"""
    return text.strip().replace("\n", " ").replace("  ", " ")