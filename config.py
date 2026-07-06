# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Updated Production Endpoint for Groq
    MODEL_NAME = "llama-3.1-8b-instant" 
    
    # RAG Tuning Parameters
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"