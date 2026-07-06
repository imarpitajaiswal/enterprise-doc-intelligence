# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    # Mixtral offers a 32k context window—perfect for processing massive corporate PDFs
    MODEL_NAME = "mixtral-8x7b-32768" 
    
    # RAG Tuning Parameters
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "all-MiniLM-L6-v2" # Fast, local, zero-cost embeddings