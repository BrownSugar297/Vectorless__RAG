"""
Query tab UI component.
"""

import html
import streamlit as st
from services.llm_service import GroqService
from config import AppConfig


def render_query_tab():
    """Render the query tab for searching and getting LLM answers."""
    if not st.session_state.chunks:
        st.info("👆 Go to **Ingest** tab first to upload a document and build the index.")
        return

    # Display info pills
    st.markdown(f"""
    <span class="info-pill">📄 {html.escape(str(st.session_state.doc_name))}</span>
    <span class="info-pill">🧩 {len(st.session_state.chunks)} chunks indexed</span>
    <span class="info-pill">🔑 {len(st.session_state.bm25.index)} unique terms</span>
    <span class="info-pill">🤖 {st.session_state.get('model', AppConfig.DEFAULT_MODEL)}</span>
    """, unsafe_allow_html=True)
    st.markdown("")

    query = st.text_input(
        "Ask a question about your document",
        placeholder="What is this document about?",
    )

    if st.button("🔍 Search & Answer") and query.strip():
        if not AppConfig.is_api_key_configured():
            st.error("No API key found. Add `GROQ_API_KEY=gsk_...` to your `.env` file and restart.")
            return

        bm25 = st.session_state.bm25
        top_k = st.session_state.get("top_k", AppConfig.DEFAULT_TOP_K)
        model = st.session_state.get("model", AppConfig.DEFAULT_MODEL)

        # Step 1: BM25 Retrieval
        with st.spinner("Retrieving relevant chunks via BM25..."):
            results = bm25.score(query)
            top_results = results[:top_k]

        if not top_results:
            st.warning("No relevant chunks found. Try rephrasing your query.")
            return

        col_ret, col_ans = st.columns([1, 1.4])

        with col_ret:
            st.markdown(f"<span class='step-badge'>STEP 1</span> **BM25 Retrieved Chunks**", unsafe_allow_html=True)
            max_score = top_results[0][0] if top_results else 1
            for rank, (score, idx) in enumerate(top_results):
                pct = int((score / max_score) * 100) if max_score > 0 else 0
                chunk_preview = st.session_state.chunks[idx]
                st.markdown(f"""
                <div class="chunk-card">
                    <div class="chunk-score">#{rank+1} · BM25: {score:.3f} · Match: {pct}%</div>
                    {html.escape(chunk_preview[:250])}{'...' if len(chunk_preview) > 250 else ''}
                    <div class="chunk-meta">chunk #{idx} · {len(chunk_preview.split())}w</div>
                </div>
                """, unsafe_allow_html=True)

        with col_ans:
            st.markdown("<span class='step-badge'>STEP 2</span> **LLM Answer**", unsafe_allow_html=True)

            # Step 2: Call Groq LLM
            with st.spinner(f"Calling {model} via Groq..."):
                try:
                    groq_service = GroqService(AppConfig.GROQ_API_KEY)
                    result = groq_service.generate_answer(
                        query=query,
                        context_chunks=top_results,
                        chunks=st.session_state.chunks,
                        model=model,
                    )
                    answer = result["answer"]
                    tokens_used = result["tokens_used"]

                    # Use st.markdown without unsafe_allow_html for answer (safer rendering)
                    st.markdown(f'<div class="answer-box">{html.escape(answer)}</div>', unsafe_allow_html=True)
                    st.caption(f"📊 Tokens: {tokens_used} · Model: {model} · Chunks: {len(top_results)}")

                    # Save to history
                    st.session_state.qa_history.append({
                        "q": query,
                        "a": answer,
                        "chunks": len(top_results),
                        "top_score": top_results[0][0],
                        "model": model,
                    })
                except Exception as e:
                    st.error(f"Groq API Error: {e}")

    # Display query history
    if st.session_state.qa_history:
        st.markdown("---")
        with st.expander(f"📜 Query History ({len(st.session_state.qa_history)} questions)"):
            for i, item in enumerate(reversed(st.session_state.qa_history)):
                q_num = len(st.session_state.qa_history) - i
                st.markdown(f"**Q{q_num}:** {html.escape(item['q'])}")
                st.markdown(f"<div style='color:#9080ff; font-size:0.8rem; margin-bottom:0.5rem'>{html.escape(item['a'][:200])}...</div>", unsafe_allow_html=True)
                st.caption(f"BM25 top score: {item['top_score']:.3f} · {item['chunks']} chunks · {item.get('model', '')}")
                st.markdown("---")
