# src/document_processor.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import Config
import tempfile
import os

def process_document(uploaded_file):
    """
    Ingests an uploaded corporate PDF, extracts text, chunks data, 
    and generates a high-dimensional FAISS vector store.
    """
    # 1. Securely save uploaded file to a temporary OS-level path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

    try:
        # 2. Data Ingestion & Chunking
        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()
        
        # Recursive splitting ensures we don't cut off sentences mid-thought
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " "]
        )
        chunks = text_splitter.split_documents(docs)
        
        # 3. Vector Embedding & Storage
        embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
        vector_store = FAISS.from_documents(chunks, embeddings)
        
        return vector_store
        
    finally:
        # 4. Strict cleanup to prevent memory leaks in production
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)