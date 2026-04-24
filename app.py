"""
Vectorless RAG - Streamlit Application
Main entry point that orchestrates all components.
"""

import streamlit as st
from config import AppConfig
from ui.styles import inject_custom_css
from ui.header import render_header
from ui.sidebar import render_sidebar
from ui.ingest_tab import render_ingest_tab
from ui.query_tab import render_query_tab
from ui.learn_tab import render_learn_tab

st.set_page_config(
    page_title=AppConfig.APP_TITLE,
    page_icon=AppConfig.APP_ICON,
    layout=AppConfig.APP_LAYOUT,
    initial_sidebar_state=AppConfig.APP_SIDEBAR_STATE,
)

inject_custom_css()


session_defaults = {
    "chunks": [],
    "bm25": None,
    "doc_name": "",
    "qa_history": [],
}

for key, default in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default


config = render_sidebar()


st.session_state["model"] = config["model"]
st.session_state["top_k"] = config["top_k"]

render_header()


tab_ingest, tab_query, tab_learn = st.tabs(["📄 Ingest", "💬 Query", "📚 How It Works"])


with tab_ingest:
    render_ingest_tab(config)


with tab_query:
    render_query_tab()

with tab_learn:
    render_learn_tab()
