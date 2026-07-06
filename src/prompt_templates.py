# src/prompt_templates.py
from langchain_core.prompts import ChatPromptTemplate

def get_enterprise_qa_prompt():
    """Defines the strict system prompt for document-based retrieval."""
    system_prompt = (
        "You are an elite Enterprise Document Intelligence Assistant. "
        "Use the provided context to answer the user's query accurately and professionally. "
        "If the answer is not contained within the context, state clearly that the information is unavailable. "
        "Do not invent or hallucinate information. Maintain an executive, concise tone.\n\n"
        "Context:\n{context}"
    )
    
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])