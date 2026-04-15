"""
How It Works educational tab UI component.
"""

import streamlit as st


def render_learn_tab():
    """Render the educational 'How It Works' tab."""
    st.markdown("""
    ## 🧠 What is Vectorless RAG?

    Traditional RAG uses **embedding models** to convert text into high-dimensional vectors,
    then a **vector database** (Pinecone, Chroma, FAISS) to find similar chunks.

    **Vectorless RAG** skips all of that — it uses **BM25**, a classical information
    retrieval algorithm from 1994 that's still used by Elasticsearch and Solr today.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### ✅ Vectorless RAG (BM25)
        - No GPU needed
        - No embedding API calls
        - No vector database setup
        - Instant, deterministic results
        - Great for keyword-heavy domains
        - Fully explainable scores
        """)
    with col2:
        st.markdown("""
        ### 🔮 Vector RAG (Embeddings)
        - Captures semantic similarity
        - Understands paraphrases
        - Requires embedding model
        - Needs vector DB infrastructure
        - Higher cost & complexity
        - Black-box similarity scores
        """)

    st.markdown("---")
    st.markdown("""
    ## 📐 BM25 Formula

    For a query term `t` in document `d`:
    """)

    st.latex(r"""
    \text{score}(D, Q) = \sum_{t \in Q} \text{IDF}(t) \cdot \frac{f(t,D) \cdot (k_1 + 1)}{f(t,D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}
    """)

    st.markdown("""
    Where:
    - **f(t,D)** = term frequency of `t` in document `D`
    - **|D|** = document length in words
    - **avgdl** = average document length across corpus
    - **k1** = controls term saturation (1.2–2.0 typical)
    - **b** = controls length normalization (0.75 typical)
    - **IDF** = inverse document frequency (penalizes common terms)
    """)

    st.markdown("---")
    st.markdown("""
    ## 🔄 The Pipeline in This App

    ```
    Document
       ↓  chunk_text()       — split into 300-word overlapping windows
    Chunks[]
       ↓  BM25.__init__()    — build inverted index, compute avgdl
    Index
       ↓  BM25.score(query)  — rank chunks by BM25 relevance
    Top-K Chunks
       ↓  build prompt       — inject chunks as context
    Claude API
       ↓
    Grounded Answer ✅
    ```

    The **inverted index** maps every unique term to the documents containing it,
    enabling fast lookup without scanning every chunk on every query.
    """)

    st.markdown("---")
    st.markdown("""
    ## 🚀 When to Use Each Approach

    | Scenario | Use Vectorless BM25 | Use Vector RAG |
    |----------|--------------------|--------------------|
    | Legal / medical exact terms | ✅ | ⚠️ |
    | Code search | ✅ | ⚠️ |
    | Semantic questions | ⚠️ | ✅ |
    | Low resource environment | ✅ | ⚠️ |
    | Fast prototyping | ✅ | ⚠️ |
    | Multilingual / paraphrase | ⚠️ | ✅ |
    """)
