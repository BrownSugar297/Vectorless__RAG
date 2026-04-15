"""
Document ingestion tab UI component.
"""

import html
import streamlit as st
from core.text_processor import chunk_text, extract_text
from core.bm25 import BM25


def render_ingest_tab(config):
    """
    Render the document ingestion tab.

    Parameters
    ----------
    config : dict
        Configuration dictionary with chunk_size, overlap, k1, b settings.

    Returns
    -------
    bool
        True if index was built successfully, False otherwise.
    """
    col_up, col_or, col_paste = st.columns([3, 0.3, 3])

    with col_up:
        st.markdown("**Upload a document**")
        uploaded = st.file_uploader(
            "Drop a .txt, .md, or .pdf file",
            type=["txt", "md", "pdf"],
            label_visibility="collapsed"
        )
        raw_text = ""
        if uploaded:
            raw_text = extract_text(uploaded)
            st.caption(f"Extracted {len(raw_text):,} characters from `{uploaded.name}`")

    with col_or:
        st.markdown("<div style='text-align:center; margin-top:2rem; color:#454560'>or</div>", unsafe_allow_html=True)

    with col_paste:
        st.markdown("**Paste text directly**")
        pasted = st.text_area(
            "Paste your text here",
            height=150,
            placeholder="Paste any text you want to query...",
            label_visibility="collapsed"
        )

    # Determine source text
    source_text = ""
    source_name = ""
    if uploaded and raw_text.strip():
        source_text = raw_text
        source_name = uploaded.name
    elif pasted.strip():
        source_text = pasted
        source_name = "Pasted Text"

    index_built = False

    if source_text:
        st.markdown("---")
        if st.button("⚡ Build Index", use_container_width=False):
            with st.spinner("Chunking and building BM25 index..."):
                chunks = chunk_text(source_text, config["chunk_size"], config["overlap"])
                bm25 = BM25(chunks, k1=config["k1"], b=config["b"])
                st.session_state.chunks = chunks
                st.session_state.bm25 = bm25
                st.session_state.doc_name = source_name
                st.session_state.qa_history = []

            st.success(f"✅ Index built! {len(chunks)} chunks from **{html.escape(source_name)}**")

            c1, c2, c3 = st.columns(3)
            c1.metric("Chunks", len(chunks))
            c2.metric("Unique Terms", len(bm25.index))
            c3.metric("Avg Chunk Length", f"{bm25.avgdl:.0f}w")

            index_built = True

    if st.session_state.chunks:
        with st.expander(f"👁 Preview chunks ({len(st.session_state.chunks)} total)"):
            for i, chunk in enumerate(st.session_state.chunks[:5]):
                st.markdown(f"""
                <div class="chunk-card">
                    <div class="chunk-score">CHUNK #{i+1}</div>
                    {html.escape(chunk[:300])}{'...' if len(chunk) > 300 else ''}
                    <div class="chunk-meta">words: {len(chunk.split())}</div>
                </div>
                """, unsafe_allow_html=True)
            if len(st.session_state.chunks) > 5:
                st.caption(f"... and {len(st.session_state.chunks) - 5} more chunks")

    return index_built
