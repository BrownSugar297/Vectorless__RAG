"""
Custom CSS styling for the Vectorless RAG application.
"""


def inject_custom_css():
    """Inject custom CSS into Streamlit app for styling."""
    import streamlit as st
    
    css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background: #0d0d14;
    color: #e8e8f0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #12121e;
    border-right: 1px solid #1e1e32;
}

/* Title */
.main-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #7c6dfa;
    letter-spacing: -1px;
    margin-bottom: 0;
}

.sub-title {
    font-size: 0.85rem;
    color: #6b6b8a;
    font-family: 'Space Mono', monospace;
    margin-bottom: 2rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Cards */
.chunk-card {
    background: #16162a;
    border: 1px solid #252540;
    border-left: 3px solid #7c6dfa;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.75rem;
    font-size: 0.85rem;
    color: #b0b0cc;
    line-height: 1.6;
}

.chunk-score {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #7c6dfa;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.chunk-meta {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #454560;
    margin-top: 0.5rem;
}

/* Answer box */
.answer-box {
    background: #13132a;
    border: 1px solid #7c6dfa44;
    border-radius: 10px;
    padding: 1.5rem;
    line-height: 1.8;
    color: #d8d8f0;
    font-size: 0.95rem;
}

/* Pipeline step */
.step-badge {
    display: inline-block;
    background: #7c6dfa22;
    border: 1px solid #7c6dfa55;
    border-radius: 4px;
    padding: 0.15rem 0.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #9080ff;
    margin-right: 0.5rem;
}

.info-pill {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #252545;
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #6b6b8a;
    margin: 0.2rem;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #12121e !important;
    border: 1px solid #252540 !important;
    color: #e8e8f0 !important;
    border-radius: 6px !important;
    font-family: 'Sora', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7c6dfa !important;
    box-shadow: 0 0 0 2px #7c6dfa22 !important;
}

.stButton > button {
    background: #7c6dfa !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    padding: 0.5rem 1.5rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #9080ff !important;
    transform: translateY(-1px);
}

.stSlider > div { color: #9080ff !important; }

div[data-testid="stMetricValue"] {
    color: #7c6dfa !important;
    font-family: 'Space Mono', monospace !important;
}

.stFileUploader {
    background: #12121e;
    border: 1px dashed #252540;
    border-radius: 8px;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #6b6b8a;
}

.stTabs [aria-selected="true"] {
    color: #7c6dfa !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #9080ff;
}

hr { border-color: #1e1e32; }
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
