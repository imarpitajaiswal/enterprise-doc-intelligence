# src/llm_engine.py
from langchain_groq import ChatGroq
from config import Config

def get_llm():
    """Initializes and returns the Groq LLM instance for enterprise inference."""
    if not Config.GROQ_API_KEY:
        raise ValueError("CRITICAL: GROQ_API_KEY is missing. Verify your .env file.")
    
    return ChatGroq(
        temperature=0.1, 
        model_name=Config.MODEL_NAME,
        groq_api_key=Config.GROQ_API_KEY
    )