"""
Chroma vector database retriever for RAG application.

This module provides semantic search functionality using ChromaDB. It encodes
user queries into embeddings and retrieves the most relevant text chunks from
the vector database to provide context for answer generation.
"""

from model.embedding_model import load_embedding_model
from vectorstore.chroma_manager import get_chroma_collection, get_chroma_client

# Initialize embedding model, database client, and collection at module level
# This ensures models are loaded once for efficiency across multiple queries
model = load_embedding_model()
client = get_chroma_client()
collection = get_chroma_collection(client)


def chroma_retriever(query):
    """
    Retrieve the most relevant text chunks for a given query.

    This function performs semantic search by:
    1. Encoding the query into a vector embedding
    2. Searching the ChromaDB collection for similar embeddings
    3. Returning the top 2 most relevant text chunks

    Args:
        query (str): The user's question or search query

    Returns:
        list[str]: Top 2 most relevant text chunks from the database.
            These chunks will be used as context for answer generation.

    Example:
        >>> results = chroma_retriever("What is the revenue?")
        >>> print(results)
        ["Revenue for Q1 was $1.2M...", "The total revenue increased by 15%..."]

    Note:
        - Queries ChromaDB for 5 results but returns only the top 2
        - Uses cosine similarity for relevance ranking
        - Returns empty list if collection is not initialized
    """
    # Convert query text to embedding vector
    query_emb = model.encode([query]).tolist()

    # Query ChromaDB collection for top 5 similar chunks
    results = collection.query(query_embeddings=query_emb, n_results=5)

    # Return only the top 2 most relevant documents
    return results['documents'][0][:2]









