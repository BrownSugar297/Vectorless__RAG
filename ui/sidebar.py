"""
Sidebar configuration UI component.
"""

import streamlit as st
from config import AppConfig


def render_sidebar():
    """Render the application sidebar with configuration controls."""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        st.markdown("---")

        # Show .env key status
        if AppConfig.is_api_key_configured():
            st.markdown("""
            <div style='background:#0f2a1a; border:1px solid #1a5c2a; border-radius:6px;
                        padding:0.5rem 0.75rem; font-family: Space Mono, monospace;
                        font-size:0.7rem; color:#4caf7d; margin-bottom:1rem;'>
                ✅ GROQ key loaded from <code>.env</code>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#2a0f0f; border:1px solid #5c1a1a; border-radius:6px;
                        padding:0.5rem 0.75rem; font-family: Space Mono, monospace;
                        font-size:0.7rem; color:#cf6679; margin-bottom:1rem;'>
                ⚠️ No key found in <code>.env</code><br>
                Add <code>GROQ_API_KEY=gsk_...</code>
            </div>
            """, unsafe_allow_html=True)

        # Model selection
        st.markdown("**Model**")
        model = st.selectbox(
            "Groq model",
            AppConfig.AVAILABLE_MODELS,
            index=AppConfig.AVAILABLE_MODELS.index(AppConfig.DEFAULT_MODEL),
            label_visibility="collapsed",
        )

        # Chunking settings
        st.markdown("**Chunking**")
        chunk_size = st.slider(
            "Chunk size (words)",
            AppConfig.CHUNK_SIZE_MIN,
            AppConfig.CHUNK_SIZE_MAX,
            AppConfig.DEFAULT_CHUNK_SIZE,
            AppConfig.CHUNK_SIZE_STEP,
        )
        overlap = st.slider(
            "Overlap (words)",
            AppConfig.OVERLAP_MIN,
            AppConfig.OVERLAP_MAX,
            AppConfig.DEFAULT_OVERLAP,
            AppConfig.OVERLAP_STEP,
        )

        # Retrieval settings
        st.markdown("**Retrieval**")
        top_k = st.slider(
            "Top-K chunks to retrieve",
            AppConfig.TOP_K_MIN,
            AppConfig.TOP_K_MAX,
            AppConfig.DEFAULT_TOP_K,
        )

        # BM25 parameters
        st.markdown("**BM25 Parameters**")
        k1 = st.slider(
            "k1 (term saturation)",
            AppConfig.K1_MIN,
            AppConfig.K1_MAX,
            AppConfig.DEFAULT_K1,
            AppConfig.K1_STEP,
        )
        b = st.slider(
            "b (length normalization)",
            AppConfig.B_MIN,
            AppConfig.B_MAX,
            AppConfig.DEFAULT_B,
            AppConfig.B_STEP,
        )

        st.markdown("---")
        
        # App info footer
        st.markdown("""
        <div style='font-family: Space Mono, monospace; font-size: 0.65rem; color: #454560; line-height: 1.8;'>
        📖 <b style='color:#7c6dfa'>Vectorless RAG</b><br>
        No embeddings. No vector DB.<br>
        Pure BM25 term matching.<br><br>
        Pipeline:<br>
        1. Chunk documents<br>
        2. Build inverted index<br>
        3. BM25 score query vs chunks<br>
        4. Send top-K → Groq LLM<br>
        5. Get grounded answer
        <br><br>
        <code style='color:#7c6dfa'>Dev: Ashikur Rahman</code>
        </div>
        """, unsafe_allow_html=True)

    return {
        "model": model,
        "chunk_size": chunk_size,
        "overlap": overlap,
        "top_k": top_k,
        "k1": k1,
        "b": b,
    }
