"""
Text processing utilities for document ingestion and chunking.
"""

import io
import re


def tokenize(text: str) -> list[str]:
    """
    Tokenize text: lowercase, split on non-alphanumeric, remove stopwords.
    
    Parameters
    ----------
    text : str
        Raw text to tokenize.
        
    Returns
    -------
    list[str]
        Cleaned token list.
    """
    STOPWORDS = {
        "the", "a", "an", "is", "it", "in", "on", "at", "to", "for", "of", "and",
        "or", "but", "with", "this", "that", "are", "was", "be", "as", "by", "from",
        "its", "also", "not", "have", "has", "been", "had", "do", "did", "does",
        "will", "would", "could", "should", "may", "might", "shall", "their",
        "they", "we", "i", "you", "he", "she", "what", "which", "who", "how",
        "when", "where", "why", "then", "than", "so", "if", "about", "into",
        "through", "more", "other", "some", "these", "those", "there", "here"
    }
    tokens = re.findall(r'[a-z0-9]+', text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping word-based chunks.
    
    Parameters
    ----------
    text : str
        Raw text to chunk.
    chunk_size : int
        Number of words per chunk.
    overlap : int
        Number of overlapping words between consecutive chunks.
        
    Returns
    -------
    list[str]
        List of text chunks.
    """
    words = text.split()
    chunks = []
    step = max(1, chunk_size - overlap)
    
    for i in range(0, len(words), step):
        chunk = " ".join(words[i: i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks


def extract_text(uploaded_file) -> str:
    """
    Extract text from uploaded file (TXT, MD, or PDF).
    
    Parameters
    ----------
    uploaded_file : Streamlit UploadedFile
        File object from Streamlit file uploader.
        
    Returns
    -------
    str
        Extracted text content.
    """
    name = uploaded_file.name.lower()
    
    if name.endswith(".txt") or name.endswith(".md"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    elif name.endswith(".pdf"):
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            return "\n".join(
                page.extract_text() or "" for page in reader.pages
            )
        except Exception as e:
            return f"[PDF extraction failed: {e}]"
    
    return uploaded_file.read().decode("utf-8", errors="ignore")
