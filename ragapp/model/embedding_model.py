"""
Embedding model loader for RAG application.

This module provides utilities for loading sentence embedding models using
the SentenceTransformers library. These embeddings are used to convert text
chunks into dense vector representations for semantic search.
"""

from sentence_transformers import SentenceTransformer


def load_embedding_model(model_name="all-MiniLM-L6-v2"):
    """
    Load a pre-trained sentence embedding model.

    This function initializes a SentenceTransformer model that converts text
    into dense vector embeddings. The default model 'all-MiniLM-L6-v2' is a
    lightweight model that produces 384-dimensional embeddings and offers a
    good balance between performance and quality.

    Args:
        model_name (str): Name of the SentenceTransformer model to load.
            Default is "all-MiniLM-L6-v2". Other options include:
            - "all-mpnet-base-v2" (higher quality, slower)
            - "paraphrase-MiniLM-L6-v2" (optimized for paraphrase detection)

    Returns:
        SentenceTransformer: The loaded embedding model ready for encoding text

    Example:
        >>> model = load_embedding_model()
        >>> embeddings = model.encode(["This is a sentence"])
        >>> embeddings.shape
        (1, 384)
    """
    print(f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    print("Model loaded successfully.")
    return model