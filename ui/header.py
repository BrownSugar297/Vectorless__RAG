"""
Header UI component.
"""

import streamlit as st


def render_header():
    """Render the application header with title and subtitle."""
    st.markdown('<div class="main-title">🔍 Vectorless RAG</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">BM25 Retrieval · No Embeddings · No Vector DB · Powered by Groq</div>', unsafe_allow_html=True)
