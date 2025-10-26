"""
Text chunking module for RAG application.

This module splits long paragraphs into smaller, semantically meaningful chunks
that fit within the embedding model's context window. It uses sentence-level
tokenization to preserve semantic coherence.
"""

import nltk

# Download NLTK's sentence tokenizer data (punkt) silently
nltk.download("punkt", quiet=True)


def chunk_text(text, max_tokens=100):
    """
    Split text into chunks with a maximum token limit.

    This function breaks down long text into smaller chunks while preserving
    sentence boundaries. Each chunk contains complete sentences and stays
    within the specified token limit.

    Args:
        text (str): The input text to be chunked
        max_tokens (int): Maximum number of tokens (words) per chunk (default: 100)

    Returns:
        list[str]: List of text chunks, each containing complete sentences

    Example:
        >>> chunk_text("First sentence. Second sentence. Third sentence.", max_tokens=5)
        ["First sentence.", "Second sentence.", "Third sentence."]
    """
    # Tokenize text into individual sentences
    sentences = nltk.sent_tokenize(text)
    chunks, current_chunk = [], []

    for sentence in sentences:
        # Check if adding this sentence would exceed max_tokens
        if len(current_chunk) + len(sentence.split()) <= max_tokens:
            current_chunk.append(sentence)
        else:
            # Save current chunk and start a new one
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def prepare_chunks(paragraphs):
    """
    Process multiple paragraphs into chunks with metadata.

    Takes a list of paragraphs and converts them into smaller chunks suitable
    for embedding and vector storage. Each chunk is assigned a unique ID and
    maintains a reference to its source paragraph.

    Args:
        paragraphs (list[dict]): List of paragraph dictionaries, each containing:
            - id (str): Unique paragraph identifier
            - text (str): The paragraph content

    Returns:
        list[dict]: List of chunk dictionaries, each containing:
            - chunk_id (str): Unique chunk identifier (format: "{para_id}_c{index}")
            - paragraph_id (str): Reference to source paragraph ID
            - text (str): The chunk content

    Example:
        >>> paras = [{"id": "1", "text": "Long paragraph..."}]
        >>> prepare_chunks(paras)
        [{"chunk_id": "1_c0", "paragraph_id": "1", "text": "First chunk..."}]
    """
    all_chunks = []
    for para in paragraphs:
        # Split paragraph into chunks of 100 tokens each
        chunks = chunk_text(para["text"], max_tokens=100)

        # Create metadata for each chunk
        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{para['id']}_c{idx}",  # Unique chunk identifier
                "paragraph_id": para["id"],          # Source paragraph reference
                "text": chunk                        # Chunk content
            })
    return all_chunks