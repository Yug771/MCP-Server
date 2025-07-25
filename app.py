import streamlit as st
import os
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="DocAssistant - Cloud Version",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as before)
st.markdown("""
<style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .doc-content {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
        color: #212529;
    }
    .search-result {
        background-color: #fff3cd;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        color: #856404;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    /* Fix for input and textarea visibility */
    .stTextInput > div > div > input {
        color: #212529 !important;
        background-color: #ffffff !important;
    }
    .stTextArea > div > div > textarea {
        color: #212529 !important;
        background-color: #ffffff !important;
    }
    h1 {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []

# Direct implementation of document operations (no MCP)
DOCS_DIR = "documents"

# Ensure documents directory exists
os.makedirs(DOCS_DIR, exist_ok=True)

def list_documents():
    """List all .txt documents"""
    try:
        return [f for f in os.listdir(DOCS_DIR) if f.endswith(".txt")]
    except Exception as e:
        st.error(f"Error listing documents: {str(e)}")
        return []

def read_document(filename):
    """Read document content"""
    try:
        path = os.path.join(DOCS_DIR, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"Error: {filename} not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"

def append_to_document(filename, content):
    """Append content to document"""
    try:
        path = os.path.join(DOCS_DIR, filename)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)
        return f"✅ Appended to {filename}."
    except Exception as e:
        return f"Error appending: {str(e)}"

def search_in_document(filename, keyword):
    """Search for keyword in document"""
    try:
        path = os.path.join(DOCS_DIR, filename)
        if not os.path.exists(path):
            return [f"Error: {filename} not found."]
        
        results = []
        with open(path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if keyword.lower() in line.lower():
                    results.append(f"{i}: {line.strip()}")
        
        return results if results else [f"No occurrences of '{keyword}' found."]
    except Exception as e:
        return [f"Error searching: {str(e)}"]

def main():
    # Header
    st.title("📄 MCP DocAssistant")
    st.markdown("**Your intelligent document companion** - Seamlessly manage, search, and organize your text documents 🚀")
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **DocAssistant Cloud** 
        
        This is a cloud-ready version that works on Streamlit Cloud!
        
        **Features:**
        - 📋 List documents
        - 👁️ View content
        - ✏️ Append text
        - 🔍 Search keywords
        
        **Note:** Documents are stored temporarily and may be reset when the app restarts.
        """)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 List Documents", "👁️ View Document", "✏️ Append to Document", "🔍 Search in Document"])
    
    # Tab 1: List Documents
    with tab1:
        st.header("📋 Available Documents")
        
        if st.button("🔄 Refresh List", key="refresh_list"):
            st.session_state.documents = list_documents()
        
        if not st.session_state.documents:
            st.session_state.documents = list_documents()
        
        if st.session_state.documents:
            cols = st.columns(3)
            for idx, doc in enumerate(st.session_state.documents):
                with cols[idx % 3]:
                    st.info(f"📄 **{doc}**")
        else:
            st.info("No documents found. Create some .txt files in the documents folder.")
    
    # Tab 2: View Document
    with tab2:
        st.header("👁️ View Document Content")
        
        docs = list_documents()
        if docs:
            selected_doc = st.selectbox("Select a document:", docs, key="view_select")
            
            if st.button("📖 Read Document", key="read_btn"):
                content = read_document(selected_doc)
                st.markdown("### Document Content:")
                st.markdown(f'<div class="doc-content">{content}</div>', unsafe_allow_html=True)
                
                # Add download button
                if not content.startswith("Error:"):
                    st.download_button(
                        label="📥 Download Document",
                        data=content,
                        file_name=selected_doc,
                        mime="text/plain"
                    )
        else:
            st.warning("No documents available.")
    
    # Tab 3: Append to Document
    with tab3:
        st.header("✏️ Append to Document")
        
        docs = list_documents()
        if docs:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                selected_doc = st.selectbox("Select a document:", docs, key="append_select")
            
            with col2:
                append_content = st.text_area(
                    "Content to append:",
                    placeholder="Enter the text you want to add to the document...",
                    height=150
                )
            
            if st.button("➕ Append to Document", key="append_btn"):
                if append_content:
                    # Add newline if content doesn't end with one
                    if not append_content.endswith('\n'):
                        append_content += '\n'
                    
                    result = append_to_document(selected_doc, append_content)
                    st.markdown(f'<div class="success-message">{result}</div>', unsafe_allow_html=True)
                    if "✅" in result:
                        st.balloons()
                else:
                    st.warning("Please enter some content to append.")
        else:
            st.warning("No documents available.")
    
    # Tab 4: Search in Document
    with tab4:
        st.header("🔍 Search in Document")
        
        docs = list_documents()
        if docs:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_doc = st.selectbox("Select a document:", docs, key="search_select")
            
            with col2:
                search_keyword = st.text_input(
                    "Search keyword:",
                    placeholder="Enter keyword to search..."
                )
            
            if st.button("🔎 Search", key="search_btn"):
                if search_keyword:
                    results = search_in_document(selected_doc, search_keyword)
                    st.markdown("### Search Results:")
                    
                    if results and "No occurrences" in results[0]:
                        st.info(results[0])
                    elif results and not results[0].startswith("Error:"):
                        st.success(f"Found {len(results)} occurrence(s):")
                        for result in results:
                            st.markdown(f'<div class="search-result">📍 {result}</div>', unsafe_allow_html=True)
                    else:
                        st.error(results[0] if results else "Error searching")
                else:
                    st.warning("Please enter a keyword to search.")
        else:
            st.warning("No documents available.")

if __name__ == "__main__":
    main() 