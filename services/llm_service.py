"""
Groq LLM service integration.
Handles all interactions with the Groq API for generating answers.
"""

from groq import Groq


class GroqService:
    """Service wrapper for Groq LLM API calls."""

    def __init__(self, api_key: str):
        """
        Initialize Groq service.
        
        Parameters
        ----------
        api_key : str
            Groq API key for authentication.
        """
        self.client = Groq(api_key=api_key)

    def generate_answer(
        self,
        query: str,
        context_chunks: list[tuple[float, int]],
        chunks: list[str],
        model: str = "llama-3.3-70b-versatile",
        max_tokens: int = 800,
        temperature: float = 0.2,
    ) -> dict:
        """
        Generate answer from LLM using retrieved context chunks.
        
        Parameters
        ----------
        query : str
            User's question.
        context_chunks : list of (score, chunk_index) tuples
            Retrieved chunks from BM25 retrieval.
        chunks : list[str]
            All document chunks (indexed by chunk_index).
        model : str
            Groq model identifier.
        max_tokens : int
            Maximum tokens in response.
        temperature : float
            Sampling temperature (lower = more deterministic).
            
        Returns
        -------
        dict
            Contains 'answer', 'tokens_used', and 'model' keys.
            
        Raises
        ------
        Exception
            If Groq API call fails.
        """
        # Build context string with chunk metadata
        context_blocks = "\n\n---\n\n".join(
            f"[Chunk #{idx}, BM25={score:.3f}]\n{chunks[idx]}"
            for score, idx in context_chunks
        )

        # Construct grounded prompt
        prompt = f"""You are a precise assistant. Answer the user's question using ONLY the provided context chunks. If the answer isn't in the context, say so clearly.

<context>
{context_blocks}
</context>

Question: {query}

Answer concisely and accurately based only on the context above."""

        # Call Groq API
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return {
            "answer": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens,
            "model": model,
        }
