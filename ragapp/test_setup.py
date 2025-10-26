#!/usr/bin/env python
"""
Quick test script to verify RAG setup is working.

This script tests each component of the RAG pipeline:
1. Embedding model loading
2. ChromaDB connection
3. LLM model loading (optional - can be slow)
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_embedding_model():
    """Test if sentence-transformers model can be loaded."""
    print("=" * 60)
    print("TEST 1: Loading Embedding Model")
    print("=" * 60)
    try:
        from model.embedding_model import load_embedding_model
        model = load_embedding_model()

        # Test encoding
        test_text = "This is a test sentence."
        embedding = model.encode([test_text])
        print(f"✓ Embedding model loaded successfully!")
        print(f"  Embedding dimension: {embedding.shape}")
        return True
    except Exception as e:
        print(f"✗ Failed to load embedding model: {e}")
        return False


def test_chromadb():
    """Test if ChromaDB can be initialized."""
    print("\n" + "=" * 60)
    print("TEST 2: ChromaDB Connection")
    print("=" * 60)
    try:
        from vectorstore.chroma_manager import get_chroma_client
        client = get_chroma_client()
        collections = client.list_collections()
        print(f"✓ ChromaDB connected successfully!")
        print(f"  Collections found: {len(collections)}")
        if collections:
            for coll in collections:
                print(f"    - {coll.name}")
        else:
            print("  ⚠ No collections found. You need to run the embedder!")
            print("    Run: python -c \"from embeder import embedder; embedder()\"")
        return True
    except Exception as e:
        print(f"✗ Failed to connect to ChromaDB: {e}")
        return False


def test_llm_model():
    """Test if LLM can be loaded (this may take time)."""
    print("\n" + "=" * 60)
    print("TEST 3: Language Model (LLM) Loading")
    print("=" * 60)
    print("⚠ This test downloads ~2.5GB on first run. Skip? (y/n): ", end="")

    try:
        response = input().lower()
        if response == 'y':
            print("Skipping LLM test...")
            return None
    except KeyboardInterrupt:
        print("\nSkipping LLM test...")
        return None

    try:
        print("Loading LLM... This may take several minutes on first run...")
        from llm.model_load import tokenizer, model
        print(f"✓ LLM loaded successfully!")
        print(f"  Model: {model.config._name_or_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to load LLM: {e}")
        print("\nTroubleshooting:")
        print("  - Ensure you have internet connection for first download")
        print("  - Check that transformers and torch are installed")
        return False


def main():
    """Run all tests."""
    print("\n🧪 RAG Setup Test Suite\n")

    results = {
        "Embedding Model": test_embedding_model(),
        "ChromaDB": test_chromadb(),
    }

    # LLM test is optional and can be None (skipped)
    llm_result = test_llm_model()
    if llm_result is not None:
        results["LLM Model"] = llm_result

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for component, status in results.items():
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {component}: {'PASS' if status else 'FAIL'}")

    all_passed = all(results.values())

    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the RAG server.")
        print("\nNext steps:")
        print("  1. Ensure ChromaDB is populated:")
        print("     python -c \"from embeder import embedder; embedder()\"")
        print("  2. Start the backend:")
        print("     cd /path/to/RAG-ragfull")
        print("     ./run_backend.sh")
        print("  3. Start the frontend:")
        print("     ./run_frontend.sh")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above before proceeding.")

    return all_passed


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
