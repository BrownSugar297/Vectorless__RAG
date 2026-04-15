# Vectorless RAG

A professional Retrieval-Augmented Generation (RAG) application using **BM25** for document retrieval — no embeddings, no vector databases.

## Features

- ✅ **Pure BM25 Retrieval** — Classical information retrieval algorithm
- ✅ **No Embeddings Required** — No GPU or embedding API calls
- ✅ **No Vector Database** — Zero infrastructure overhead
- ✅ **Groq LLM Integration** — Fast, grounded answers via LLM
- ✅ **Deterministic & Explainable** — Transparent scoring
- ✅ **Document Support** — TXT, MD, PDF files
- ✅ **Interactive UI** — Streamlit-based interface

## System Architecture

### High-Level Flow

```mermaid
flowchart LR
    A[User] -->|Uploads Document| B[Document Ingestion]
    A -->|Asks Question| C[Query Interface]
    B -->|Raw Text| D[Text Chunking]
    D -->|Chunks| E[BM25 Index Builder]
    E -->|Inverted Index| F[(BM25 Engine)]
    C -->|Query| F
    F -->|Top-K Chunks| G[Context Assembly]
    G -->|Prompt| H[Groq LLM]
    H -->|Answer| A

    style A fill:#7c6dfa,color:#fff
    style F fill:#ff6b6b,color:#fff
    style H fill:#4caf50,color:#fff
```

### RAG Pipeline

```mermaid
flowchart TD
    A[Document<br/>TXT/MD/PDF] --> B[chunk_text<br/>Split into 300-word<br/>overlapping windows]
    B --> C[BM25.__init__<br/>Build inverted index<br/>Compute avgdl]
    C --> D[(BM25 Index<br/>Term to doc_id freq mapping)]

    E[User Query] --> F[BM25.score<br/>Rank chunks by<br/>relevance]
    D --> F
    F --> G[Top-K Chunks<br/>Retrieval]

    G --> H[Build Prompt<br/>Inject chunks as context]
    H --> I[Groq LLM<br/>llama-3.3-70b]
    I --> J[Grounded Answer<br/>With source citations]

    style A fill:#7c6dfa,color:#fff
    style E fill:#ff6b6b,color:#fff
    style D fill:#ffd93d,color:#000
    style I fill:#4caf50,color:#fff
    style J fill:#4caf50,color:#fff
```

### Application Flow (User Journey)

```mermaid
sequenceDiagram
    participant U as User
    participant S as Streamlit UI
    participant TP as Text Processor
    participant BM as BM25 Engine
    participant GS as Groq Service

    U->>S: 1. Upload document (TXT/MD/PDF)
    S->>TP: extract_text()
    TP-->>S: Raw text

    U->>S: 2. Click "Build Index"
    S->>TP: chunk_text()
    TP-->>S: List of chunks
    S->>BM: BM25(chunks, k1, b)
    BM->>BM: Build inverted index
    BM-->>S: BM25 instance

    U->>S: 3. Ask question
    S->>BM: bm25.score(query)
    BM->>BM: Calculate BM25 scores
    BM-->>S: Ranked chunks (Top-K)
    S->>S: Display retrieved chunks

    S->>GS: generate_answer(query, chunks)
    GS->>GS: Build prompt with context
    GS-->>S: LLM answer
    S-->>U: Display answer

    Note over U,GS: All BM25 scores shown for transparency
```

### Modular Codebase Structure

```mermaid
flowchart LR
    A[app.py<br/>Orchestrator] --> B[config.py<br/>Configuration]
    A --> C[ui<br/>UI Components]
    A --> D[core<br/>RAG Engine]
    A --> E[services<br/>LLM Service]

    C --> C1[styles.py]
    C --> C2[header.py]
    C --> C3[sidebar.py]
    C --> C4[ingest_tab.py]
    C --> C5[query_tab.py]
    C --> C6[learn_tab.py]

    D --> D1[bm25.py]
    D --> D2[text_processor.py]

    E --> E1[llm_service.py]

    style A fill:#7c6dfa,color:#fff
    style D fill:#ff6b6b,color:#fff
    style E fill:#4caf50,color:#fff
    style C fill:#ffd93d,color:#000
```

### BM25 Retrieval Mechanism

```mermaid
flowchart TD
    A[Query Text] --> B[Tokenize<br/>Lowercase + remove stopwords]
    B --> C[For each term t]

    C --> D{t in index?}
    D -->|No| E[Skip term]
    D -->|Yes| F[Calculate IDF<br/>log(N - n_t + 0.5 / n_t + 0.5 + 1)]

    F --> G[For each doc containing t]
    G --> H[Calculate TF<br/>freq * k1 + 1 / freq + k1*1-b+b*dl/avgdl]

    H --> I[Score += IDF * TF]
    I --> J[Next doc]
    J --> G

    E --> K{More terms?}
    K -->|Yes| C
    K -->|No| L[Rank all docs by score]
    L --> M[Return Top-K chunks]

    style A fill:#7c6dfa,color:#fff
    style M fill:#4caf50,color:#fff
    style F fill:#ffd93d,color:#000
    style H fill:#ff6b6b,color:#fff
```

## Architecture

```
vectorless-rag/
├── app.py                  # Main orchestrator (clean & minimal)
├── config.py               # Centralized configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (GROQ_API_KEY)
│
├── core/                   # Core RAG engine
│   ├── __init__.py
│   ├── bm25.py            # BM25 ranking algorithm
│   └── text_processor.py  # Text chunking & extraction
│
├── services/               # External service integrations
│   ├── __init__.py
│   └── llm_service.py     # Groq API wrapper
│
└── ui/                     # UI components
    ├── __init__.py
    ├── styles.py          # Custom CSS styling
    ├── header.py          # App header component
    ├── sidebar.py         # Configuration sidebar
    ├── ingest_tab.py      # Document ingestion UI
    ├── query_tab.py       # Search & answer UI
    └── learn_tab.py       # Educational content
```

## Setup

### 1. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from [Groq Console](https://console.groq.com/)

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

### Workflow

1. **Ingest** → Upload a document (TXT/MD/PDF) or paste text
2. **Build Index** → Chunks text and builds BM25 inverted index
3. **Query** → Ask questions, retrieve relevant chunks, get LLM answers
4. **Learn** → Understand how BM25 and Vectorless RAG work

## Configuration

### Sidebar Settings

- **Model Selection** — Choose Groq LLM model
- **Chunking** — Adjust chunk size and overlap (in words)
- **Retrieval** — Set top-K chunks to retrieve
- **BM25 Parameters** — Fine-tune k1 and b parameters

### BM25 Parameters

- **k1** (term saturation): Controls TF saturation (0.5–3.0, default: 1.5)
- **b** (length normalization): Controls length normalization (0.0–1.0, default: 0.75)

## BM25 Algorithm

The BM25 score for a query Q and document D:

```
score(D, Q) = Σ IDF(t) * [f(t,D) * (k1 + 1)] / [f(t,D) + k1 * (1 - b + b * |D|/avgdl)]
```

Where:
- **f(t,D)** = term frequency of t in D
- **|D|** = document length in words
- **avgdl** = average document length
- **IDF(t)** = inverse document frequency of term t

## Advantages of Vectorless RAG

| Feature | Vectorless BM25 | Vector RAG |
|---------|----------------|------------|
| GPU Required | ❌ | ✅ |
| Embedding API | ❌ | ✅ |
| Vector DB Setup | ❌ | ✅ |
| Deterministic | ✅ | ❌ |
| Explainable Scores | ✅ | ❌ |
| Exact Keyword Match | ✅ | ⚠️ |
| Semantic Understanding | ⚠️ | ✅ |

## Tech Stack

- **Frontend**: Streamlit
- **Retrieval**: BM25 (from scratch)
- **LLM**: Groq (Llama, Mixtral, Gemma)
- **Text Processing**: PyPDF2, Regex
- **Configuration**: python-dotenv

## Developer

**Ashikur Rahman**

## License

MIT License
