"""
ChromaDB vector store management for RAG application.

This module provides utilities for managing ChromaDB collections, including
client initialization, collection creation/reset, and embedding insertion.
ChromaDB is used to store and query vector embeddings for semantic search.
"""

import chromadb


def get_chroma_client(path="./chroma_db"):
    """
    Initialize a persistent ChromaDB client.

    Creates or connects to a ChromaDB instance that persists data to disk.
    This allows the vector database to be reused across application restarts.

    Args:
        path (str): Directory path where ChromaDB will store its data files.
            Default is "./chroma_db" in the current working directory.

    Returns:
        chromadb.PersistentClient: ChromaDB client instance for database operations

    Example:
        >>> client = get_chroma_client(path="/data/chroma")
        >>> client.list_collections()
    """
    return chromadb.PersistentClient(path=path)


def reset_collection(client, name="finance_docs"):
    """
    Delete and recreate a ChromaDB collection.

    This function is used during data ingestion to ensure a fresh collection
    without duplicate entries. It safely deletes the existing collection if
    it exists, then creates a new empty collection.

    Args:
        client (chromadb.PersistentClient): ChromaDB client instance
        name (str): Name of the collection to reset. Default is "finance_docs"

    Returns:
        chromadb.Collection: Newly created empty collection

    Example:
        >>> client = get_chroma_client()
        >>> collection = reset_collection(client, "my_docs")
        >>> print(collection.count())
        0

    Note:
        - This operation is destructive and cannot be undone
        - Use only during initial data ingestion or when refreshing the database
    """
    try:
        # Attempt to delete existing collection
        client.delete_collection(name)
    except Exception:
        # Collection doesn't exist, which is fine
        print("Collection not found. Creating new one...")

    # Create a fresh collection
    return client.create_collection(name=name)


def insert_embeddings(collection, texts, embeddings, chunks):
    """
    Insert text chunks and their embeddings into ChromaDB collection.

    This function bulk-inserts document chunks along with their vector embeddings
    and metadata into the specified ChromaDB collection. Each chunk is assigned
    a unique ID and maintains a reference to its source paragraph.

    Args:
        collection (chromadb.Collection): Target ChromaDB collection
        texts (list[str]): List of text chunks to insert
        embeddings (list[list[float]]): Corresponding embedding vectors for each chunk
        chunks (list[dict]): List of chunk metadata dictionaries containing:
            - chunk_id (str): Unique identifier for the chunk
            - paragraph_id (str): Reference to source paragraph

    Returns:
        None

    Side Effects:
        - Inserts documents into ChromaDB collection
        - Prints confirmation message with insertion count

    Example:
        >>> collection = get_chroma_collection(client)
        >>> insert_embeddings(
        ...     collection,
        ...     texts=["chunk text..."],
        ...     embeddings=[[0.1, 0.2, ...]],
        ...     chunks=[{"chunk_id": "1_c0", "paragraph_id": "1"}]
        ... )
        Inserted 1 chunks into Chroma.

    Note:
        - All three lists (texts, embeddings, chunks) must have the same length
        - IDs must be unique within the collection to avoid conflicts
    """
    collection.add(
        documents=texts,                                        # Text content
        embeddings=embeddings,                                  # Vector embeddings
        ids=[c["chunk_id"] for c in chunks],                   # Unique chunk IDs
        metadatas=[{"paragraph_id": c["paragraph_id"]} for c in chunks],  # Metadata
    )
    print(f"Inserted {len(chunks)} chunks into Chroma.")


def get_chroma_collection(client, name="finance_docs"):
    """
    Retrieve an existing ChromaDB collection by name.

    This function attempts to load a previously created collection from the
    ChromaDB client. Used during query/retrieval operations.

    Args:
        client (chromadb.PersistentClient): ChromaDB client instance
        name (str): Name of the collection to retrieve. Default is "finance_docs"

    Returns:
        chromadb.Collection or None: The requested collection if it exists,
            otherwise None

    Example:
        >>> client = get_chroma_client()
        >>> collection = get_chroma_collection(client, "my_docs")
        >>> if collection:
        ...     results = collection.query(...)

    Note:
        - Returns None if the collection doesn't exist (not an error)
        - Always check for None before using the returned collection
    """
    try:
        # Attempt to retrieve the collection
        collection = client.get_collection(name=name)
        return collection
    except Exception:
        # Collection doesn't exist
        print("Collection not found.")
        return None
    
