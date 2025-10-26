"""
Embedding pipeline orchestrator for RAG application.

This module coordinates the complete embedding and indexing pipeline:
1. Load and filter TATQA dataset
2. Process and chunk paragraphs
3. Generate embeddings using SentenceTransformers
4. Store embeddings in ChromaDB vector database

This is the main data ingestion script that should be run once to populate
the vector database before starting the RAG server.

Usage:
    from embeder import embedder
    embedder()
"""

from pathlib import Path
from data.loader import load_json, filter_text_questions
from data.prepare_data import process_paragraphs_and_questions
from data.chunker import prepare_chunks
from model.embedding_model import load_embedding_model
from vectorstore.chroma_manager import get_chroma_client, reset_collection, insert_embeddings
from evaluation.evaluate import run_evaluation
import sys
import os

# Add parent directory to Python path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def embedder():
    """
    Run the complete embedding and indexing pipeline.

    This function orchestrates the entire data ingestion process:
    1. Loads the TATQA dataset from JSON
    2. Filters to retain only text-based questions
    3. Processes paragraphs and questions to create chunks
    4. Generates embeddings for all chunks
    5. Stores embeddings in ChromaDB for retrieval

    The pipeline processes the test/gold dataset and populates the vector
    database used for semantic search during query time.

    Returns:
        None

    Side Effects:
        - Loads and parses dataset from ./dataset/tatqa_dataset_test_gold.json
        - Downloads sentence-transformers model if not cached
        - Creates/resets ChromaDB collection named "finance_docs"
        - Inserts all chunk embeddings into the database
        - Prints progress messages to console

    Example:
        >>> from embeder import embedder
        >>> embedder()
        embedder started
        Loading embedding model: all-MiniLM-L6-v2
        Model loaded successfully.
        Collection not found. Creating new one...
        Inserted 1234 chunks into Chroma.

    Note:
        - This is a one-time data ingestion script
        - Should be run before starting the RAG server
        - Will reset any existing collection (data loss!)
        - Takes several minutes depending on dataset size
    """
    # Step 1: Load and filter dataset
    print("embedder started")
    dev_file = Path("./dataset/tatqa_dataset_test_gold.json")
    data = load_json(dev_file)
    data = filter_text_questions(data)  # Keep only text-answerable questions

    # Step 2: Process and chunk data
    paragraphs, questions = process_paragraphs_and_questions(data)
    all_chunks = prepare_chunks(paragraphs)  # Create 100-token chunks

    # Step 3: Generate embeddings
    model = load_embedding_model()
    texts = [c["text"] for c in all_chunks]  # Extract text from chunks
    embeddings = model.encode(texts).tolist()  # Create 384-dim vectors

    # Step 4: Store in ChromaDB
    client = get_chroma_client()
    collection = reset_collection(client)  # Reset existing collection
    insert_embeddings(collection, texts, embeddings, all_chunks)

    print("Embedding pipeline completed successfully!")

    # Optional: Run retrieval evaluation
    # To enable evaluation, prepare ground_truth and retrieval_results
    # run_evaluation(ground_truth, retrieval_results)
