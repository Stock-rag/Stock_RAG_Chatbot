#!/usr/bin/env python
"""
RAGAS Evaluation Script for AskFinn RAG System

This script evaluates the RAG system using the RAGAS framework, which provides
specialized metrics for retrieval-augmented generation:
- Faithfulness: Are answers grounded in retrieved context?
- Answer Relevancy: Do answers address the question?
- Context Precision: Are relevant chunks ranked higher?
- Context Recall: Is all relevant information retrieved?

Usage:
    pip install ragas langchain langchain-community
    python run_ragas_evaluation.py --num_samples 20

Note: Requires OpenAI API key or can use local models
"""

import sys
import json
import os
from pathlib import Path
from typing import List, Dict
import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Import RAG components
from data.loader import load_json, filter_text_questions
from model.embedding_model import load_embedding_model
from vectorstore.chroma_manager import get_chroma_collection, get_chroma_client
from llm.model_load import generate_answer

# Import RAGAS
try:
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    )
    from datasets import Dataset
    RAGAS_AVAILABLE = True
except ImportError:
    print("⚠️  RAGAS not installed.")
    print("Install with: pip install ragas langchain langchain-community")
    RAGAS_AVAILABLE = False
    sys.exit(1)

# Check for OpenAI API key (needed for some RAGAS metrics)
if "OPENAI_API_KEY" not in os.environ:
    print("\n" + "=" * 70)
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment")
    print("=" * 70)
    print("\nRAGAS uses LLM-as-judge for some metrics (faithfulness, answer relevancy).")
    print("\nOptions:")
    print("1. Set OpenAI API key: export OPENAI_API_KEY='your-key'")
    print("2. Use local models (experimental)")
    print("3. Use simpler metrics (context precision/recall only)")
    print("\nContinuing with available metrics...")
    print("=" * 70 + "\n")


class RAGASEvaluator:
    """
    RAGAS-based evaluator for RAG systems.
    """

    def __init__(self, dataset_path: str = "dataset/tatqa_dataset_dev.json"):
        """Initialize evaluator with dataset and models."""
        print("=" * 70)
        print("RAGAS EVALUATION PIPELINE")
        print("=" * 70)

        # Load dataset
        print("\n[1/4] Loading TAT-QA dataset...")
        self.dataset_path = Path(dataset_path)
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")

        self.data = load_json(self.dataset_path)
        self.data = filter_text_questions(self.data)
        print(f"✓ Loaded {len(self.data)} documents")

        # Initialize models
        print("\n[2/4] Loading embedding model...")
        self.embedding_model = load_embedding_model()
        print("✓ Embedding model loaded")

        print("\n[3/4] Connecting to ChromaDB...")
        self.chroma_client = get_chroma_client()
        self.collection = get_chroma_collection(self.chroma_client)
        print(f"✓ Connected to collection: {self.collection.name}")

        print("\n[4/4] Preparation complete!")
        print("=" * 70)

    def retrieve_chunks(self, query: str, k: int = 5) -> tuple:
        """Retrieve relevant chunks for a query."""
        query_emb = self.embedding_model.encode([query]).tolist()
        results = self.collection.query(query_embeddings=query_emb, n_results=k)

        chunk_texts = results['documents'][0] if results['documents'] else []
        chunk_ids = results['ids'][0] if results['ids'] else []

        return chunk_texts, chunk_ids

    def prepare_ragas_dataset(self, num_samples: int = 20) -> Dataset:
        """
        Prepare dataset in RAGAS format.

        RAGAS expects:
        - question: The user's question
        - answer: The generated answer
        - contexts: List of retrieved chunks
        - ground_truth: Reference answer (optional)
        """
        print("\n" + "=" * 70)
        print("PREPARING RAGAS DATASET")
        print("=" * 70)

        questions = []
        answers = []
        contexts_list = []
        ground_truths = []

        sample_count = 0
        for doc in self.data:
            if sample_count >= num_samples:
                break

            for q_item in doc.get("questions", []):
                if sample_count >= num_samples:
                    break

                question = q_item.get("question", "")
                reference_answer = q_item.get("answer", "")

                # Convert reference answer to string if it's a list
                if isinstance(reference_answer, list):
                    reference_answer = " ".join(str(x) for x in reference_answer)
                elif not isinstance(reference_answer, str):
                    reference_answer = str(reference_answer)

                if not question or not reference_answer:
                    continue

                # Retrieve context
                chunk_texts, _ = self.retrieve_chunks(question, k=5)
                contexts = chunk_texts[:2]  # Use top 2 for generation

                if not contexts:
                    continue

                # Generate answer
                print(f"\n[{sample_count + 1}/{num_samples}] Processing question...")
                print(f"  Question: {question[:60]}...")

                context_str = "\n".join(contexts)
                generated_answer = generate_answer(context_str, question, max_new_tokens=100)

                # Store for RAGAS
                questions.append(question)
                answers.append(generated_answer)
                contexts_list.append(contexts)
                ground_truths.append(reference_answer)

                sample_count += 1

        print(f"\n✓ Prepared {len(questions)} samples")

        # Create RAGAS dataset
        data_dict = {
            "question": questions,
            "answer": answers,
            "contexts": contexts_list,
            "ground_truth": ground_truths
        }

        dataset = Dataset.from_dict(data_dict)
        return dataset

    def run_ragas_evaluation(self, num_samples: int = 20):
        """
        Run RAGAS evaluation.
        """
        # Prepare dataset
        dataset = self.prepare_ragas_dataset(num_samples)

        print("\n" + "=" * 70)
        print("RUNNING RAGAS EVALUATION")
        print("=" * 70)
        print("\n⚠️  This may take several minutes...")
        print("   (RAGAS uses LLM calls for faithfulness and relevancy metrics)\n")

        # Select metrics based on available API keys
        metrics_to_use = []

        if "OPENAI_API_KEY" in os.environ:
            metrics_to_use = [
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall
            ]
            print("✓ Using all RAGAS metrics (OpenAI API available)")
        else:
            # Use only metrics that don't require LLM
            metrics_to_use = [
                context_precision,
                context_recall
            ]
            print("⚠️  Using limited metrics (context precision/recall only)")
            print("   Install OpenAI API key for full evaluation")

        # Run evaluation
        try:
            results = evaluate(dataset, metrics=metrics_to_use)

            print("\n" + "=" * 70)
            print("RAGAS EVALUATION RESULTS")
            print("=" * 70)

            # Print results
            for metric_name, score in results.items():
                print(f"  {metric_name}: {score:.4f}")

            # Calculate overall score
            overall_score = sum(results.values()) / len(results)
            print(f"\n  Overall RAGAS Score: {overall_score:.4f}")

            # Save results
            output = {
                "ragas_scores": dict(results),
                "overall_score": overall_score,
                "num_samples": num_samples,
                "metrics_used": [m.name for m in metrics_to_use]
            }

            output_path = Path("ragas_results.json")
            with open(output_path, "w") as f:
                json.dump(output, f, indent=2)

            print(f"\n💾 Results saved to: {output_path}")

            # Also save as CSV for easy viewing
            df = pd.DataFrame([results])
            df.to_csv("ragas_results.csv", index=False)
            print(f"💾 Results saved to: ragas_results.csv")

            return results

        except Exception as e:
            print(f"\n❌ Error during RAGAS evaluation: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description="Run RAGAS evaluation")
    parser.add_argument("--num_samples", type=int, default=20,
                       help="Number of samples to evaluate (default: 20)")
    parser.add_argument("--dataset", type=str, default="dataset/tatqa_dataset_dev.json",
                       help="Path to TAT-QA dataset")

    args = parser.parse_args()

    if not RAGAS_AVAILABLE:
        print("RAGAS is not installed. Please install it first:")
        print("  pip install ragas langchain langchain-community")
        sys.exit(1)

    try:
        evaluator = RAGASEvaluator(dataset_path=args.dataset)
        results = evaluator.run_ragas_evaluation(num_samples=args.num_samples)

        if results:
            print("\n" + "=" * 70)
            print("EVALUATION COMPLETE!")
            print("=" * 70)
            print("\nNext steps:")
            print("1. Check ragas_results.json for detailed scores")
            print("2. Update FINDINGS_LATEX.tex with actual scores")
            print("3. Use these numbers in your WIL report")
            print("\n" + "=" * 70)

    except KeyboardInterrupt:
        print("\n\n⚠️  Evaluation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
