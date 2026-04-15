"""
BM25 (Best Matching 25) retrieval algorithm implementation.
Pure Python implementation without vector databases or embeddings.
"""

import math
from collections import Counter


class BM25:
    """
    BM25 ranking algorithm from scratch.
    
    Parameters
    ----------
    k1 : float
        Term frequency saturation parameter (default: 1.5)
        Controls how quickly term frequency saturates.
        Higher values = more weight for frequent terms.
    b : float
        Length normalization parameter (default: 0.75)
        0 = no normalization, 1 = full normalization.
    """

    def __init__(self, chunks: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.chunks = chunks
        self.N = len(chunks)
        self.tokenized = [self._tokenize(c) for c in chunks]
        self.dl = [len(t) for t in self.tokenized]
        self.avgdl = sum(self.dl) / self.N if self.N else 1
        
        # Build inverted index: term -> {doc_id: frequency}
        self.index: dict[str, dict[int, int]] = {}
        for doc_id, tokens in enumerate(self.tokenized):
            freq = Counter(tokens)
            for term, cnt in freq.items():
                self.index.setdefault(term, {})[doc_id] = cnt

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Lowercase + split on non-alphanumeric, remove stopwords."""
        STOPWORDS = {
            "the", "a", "an", "is", "it", "in", "on", "at", "to", "for", "of", "and",
            "or", "but", "with", "this", "that", "are", "was", "be", "as", "by", "from",
            "its", "also", "not", "have", "has", "been", "had", "do", "did", "does",
            "will", "would", "could", "should", "may", "might", "shall", "their",
            "they", "we", "i", "you", "he", "she", "what", "which", "who", "how",
            "when", "where", "why", "then", "than", "so", "if", "about", "into",
            "through", "more", "other", "some", "these", "those", "there", "here"
        }
        import re
        tokens = re.findall(r'[a-z0-9]+', text.lower())
        return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

    def idf(self, term: str) -> float:
        """
        Calculate Inverse Document Frequency for a term.
        
        IDF penalizes common terms and rewards rare terms.
        """
        n_t = len(self.index.get(term, {}))
        if n_t == 0:
            return 0.0
        return math.log((self.N - n_t + 0.5) / (n_t + 0.5) + 1)

    def score(self, query: str) -> list[tuple[float, int]]:
        """
        Score and rank chunks by BM25 relevance to query.
        
        Returns
        -------
        list of (score, chunk_index) tuples, sorted by score descending.
        """
        q_tokens = self._tokenize(query)
        scores = [0.0] * self.N
        
        for term in q_tokens:
            idf_val = self.idf(term)
            for doc_id, freq in self.index.get(term, {}).items():
                # BM25 term frequency normalization
                tf_norm = (freq * (self.k1 + 1)) / (
                    freq + self.k1 * (1 - self.b + self.b * self.dl[doc_id] / self.avgdl)
                )
                scores[doc_id] += idf_val * tf_norm
        
        # Rank by score, filter out zero-score chunks
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return [(score, idx) for idx, score in ranked if score > 0]
