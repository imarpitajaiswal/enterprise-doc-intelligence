# app.py
import streamlit as st
from src.document_processor import process_document
from src.llm_engine import get_llm
from src.prompt_templates import get_enterprise_qa_prompt
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage

# 1. UI Configuration
st.set_page_config(
    page_title="Enterprise Doc Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📄 Enterprise Document Intelligence")
st.markdown("### Secure, Localized RAG Pipeline for Executive Workflows")

# 2. Session State Management
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# 3. Sidebar: Document Ingestion
with st.sidebar:
    st.header("Data Ingestion")
    uploaded_file = st.file_uploader("Upload Corporate Document (PDF)", type=["pdf"])
    
    if st.button("Process Document") and uploaded_file:
        with st.spinner("Ingesting and vectorizing document..."):
            st.session_state.vector_store = process_document(uploaded_file)
            st.success("Document successfully processed and embedded.")

# 4. Chat Interface
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("User"):
            st.write(message.content)
    else:
        with st.chat_message("AI"):
            st.write(message.content)

user_query = st.chat_input("Query the document database...")

if user_query:
    # Append user query to UI
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("User"):
        st.write(user_query)

    # 5. RAG Execution Pipeline
    if st.session_state.vector_store is not None:
        with st.chat_message("AI"):
            with st.spinner("Retrieving context and generating response..."):
                try:
                    # Initialize LLM and Prompt
                    llm = get_llm()
                    prompt = get_enterprise_qa_prompt()
                    
                    # Set up chains
                    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
                    document_chain = create_stuff_documents_chain(llm, prompt)
                    retrieval_chain = create_retrieval_chain(retriever, document_chain)
                    
                    # Execute
                    response = retrieval_chain.invoke({"input": user_query})
                    answer = response["answer"]
                    
                    st.write(answer)
                    st.session_state.chat_history.append(AIMessage(content=answer))
                    
                except Exception as e:
                    st.error(f"Inference Error: {str(e)}")
    else:
        with st.chat_message("AI"):
            warning_msg = "Please upload and process a document before querying."
            st.warning(warning_msg)
            st.session_state.chat_history.append(AIMessage(content=warning_msg))