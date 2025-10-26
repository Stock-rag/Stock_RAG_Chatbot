#!/usr/bin/env python
"""
Comprehensive RAG System Evaluation Script

This script evaluates the complete RAG pipeline including:
1. Retrieval Quality: Precision@k, Recall@k, MRR
2. Generation Quality: ROUGE scores, BERTScore
3. End-to-End Performance: Response time, accuracy

Usage:
    python run_full_evaluation.py --num_samples 50

Requirements:
    pip install rouge-score bert-score nltk
"""

import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

# Import RAG components
from data.loader import load_json, filter_text_questions
from model.embedding_model import load_embedding_model
from vectorstore.chroma_manager import get_chroma_collection, get_chroma_client
from llm.model_load import generate_answer
from evaluation.metrics import evaluate_retrieval, calculate_mean

# Import evaluation libraries
try:
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: rouge-score not installed. Install with: pip install rouge-score")
    ROUGE_AVAILABLE = False

try:
    from bert_score import score as bert_score
    BERTSCORE_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: bert-score not installed. Install with: pip install bert-score")
    BERTSCORE_AVAILABLE = False


class RAGEvaluator:
    """
    Comprehensive evaluator for RAG system performance.

    Evaluates both retrieval quality and generation quality using
    standard NLP metrics.
    """

    def __init__(self, dataset_path: str = "dataset/tatqa_dataset_dev.json"):
        """Initialize evaluator with dataset and models."""
        print("=" * 70)
        print("RAG SYSTEM EVALUATION PIPELINE")
        print("=" * 70)

        # Load dataset
        print("\n[1/5] Loading TAT-QA dataset...")
        self.dataset_path = Path(dataset_path)
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")

        self.data = load_json(self.dataset_path)
        self.data = filter_text_questions(self.data)
        print(f"✓ Loaded {len(self.data)} documents")

        # Initialize models
        print("\n[2/5] Loading embedding model...")
        self.embedding_model = load_embedding_model()
        print("✓ Embedding model loaded")

        print("\n[3/5] Connecting to ChromaDB...")
        self.chroma_client = get_chroma_client()
        self.collection = get_chroma_collection(self.chroma_client)
        print(f"✓ Connected to collection: {self.collection.name}")
        print(f"  Total chunks in database: {self.collection.count()}")

        # Initialize ROUGE scorer if available
        if ROUGE_AVAILABLE:
            print("\n[4/5] Initializing ROUGE scorer...")
            self.rouge_scorer = rouge_scorer.RougeScorer(
                ['rouge1', 'rouge2', 'rougeL'],
                use_stemmer=True
            )
            print("✓ ROUGE scorer ready")
        else:
            self.rouge_scorer = None

        print("\n[5/5] Preparation complete!")
        print("=" * 70)

    def retrieve_chunks(self, query: str, k: int = 5) -> Tuple[List[str], List[str]]:
        """
        Retrieve relevant chunks for a query.

        Args:
            query: Question text
            k: Number of chunks to retrieve

        Returns:
            Tuple of (chunk_texts, chunk_ids)
        """
        query_emb = self.embedding_model.encode([query]).tolist()
        results = self.collection.query(query_embeddings=query_emb, n_results=k)

        chunk_texts = results['documents'][0] if results['documents'] else []
        chunk_ids = results['ids'][0] if results['ids'] else []

        return chunk_texts, chunk_ids

    def evaluate_retrieval_performance(self, num_samples: int = 50) -> Dict:
        """
        Evaluate retrieval quality using Precision@k, Recall@k, and MRR.

        Args:
            num_samples: Number of questions to evaluate (default: 50)

        Returns:
            Dictionary with retrieval metrics
        """
        print("\n" + "=" * 70)
        print("RETRIEVAL QUALITY EVALUATION")
        print("=" * 70)

        precision_scores = []
        recall_scores = []
        mrr_scores = []

        # Prepare ground truth and run retrieval
        sample_count = 0
        for doc in self.data:
            if sample_count >= num_samples:
                break

            doc_id = doc.get("uid", "unknown")
            doc_paragraphs = doc.get("paragraphs", [])

            # Get all paragraph texts from this document
            paragraph_texts = []
            for para in doc_paragraphs:
                if isinstance(para, dict):
                    paragraph_texts.append(para.get("text", ""))
                else:
                    paragraph_texts.append(str(para))

            for q_item in doc.get("questions", []):
                if sample_count >= num_samples:
                    break

                question = q_item.get("question", "")
                if not question:
                    continue

                # Retrieve chunks for this question
                chunk_texts, retrieved_ids = self.retrieve_chunks(question, k=5)
                top_2_chunks = chunk_texts[:2]

                # Calculate relevance: how many of the top 2 retrieved chunks
                # come from the source document?
                relevant_retrieved = 0
                first_relevant_rank = None

                for rank, chunk_text in enumerate(top_2_chunks, start=1):
                    # Check if this chunk is similar to any paragraph in the source doc
                    is_relevant = False
                    for para_text in paragraph_texts:
                        if para_text and chunk_text and len(chunk_text) > 20:
                            # Check if chunk contains significant portion of paragraph
                            # or paragraph contains significant portion of chunk
                            overlap = len(set(chunk_text.split()) & set(para_text.split()))
                            min_len = min(len(chunk_text.split()), len(para_text.split()))
                            if min_len > 0 and overlap / min_len > 0.5:
                                is_relevant = True
                                break

                    if is_relevant:
                        relevant_retrieved += 1
                        if first_relevant_rank is None:
                            first_relevant_rank = rank

                # Precision@2: fraction of retrieved that are relevant
                precision = relevant_retrieved / 2.0 if len(top_2_chunks) > 0 else 0.0

                # Recall@2: fraction of relevant docs that were retrieved
                # For simplicity, assume there are len(paragraphs) relevant chunks
                num_relevant = max(len(paragraph_texts), 1)
                recall = relevant_retrieved / num_relevant

                # MRR: reciprocal rank of first relevant result
                mrr = 1.0 / first_relevant_rank if first_relevant_rank else 0.0

                precision_scores.append(precision)
                recall_scores.append(recall)
                mrr_scores.append(mrr)

                sample_count += 1
                if sample_count % 10 == 0:
                    print(f"  Processed {sample_count}/{num_samples} questions...")

        print(f"\n✓ Evaluated {len(precision_scores)} questions")

        # Calculate mean metrics
        metrics = {
            "precision@2": np.mean(precision_scores) if precision_scores else 0.0,
            "recall@2": np.mean(recall_scores) if recall_scores else 0.0,
            "mrr": np.mean(mrr_scores) if mrr_scores else 0.0
        }

        print("\nRETRIEVAL METRICS:")
        print(f"  Precision@2: {metrics['precision@2']:.4f}")
        print(f"  Recall@2:    {metrics['recall@2']:.4f}")
        print(f"  MRR:         {metrics['mrr']:.4f}")

        return metrics

    def evaluate_generation_quality(self, num_samples: int = 20) -> Dict:
        """
        Evaluate answer generation quality using ROUGE and BERTScore.

        Args:
            num_samples: Number of questions to generate answers for

        Returns:
            Dictionary with generation metrics
        """
        print("\n" + "=" * 70)
        print("GENERATION QUALITY EVALUATION")
        print("=" * 70)

        if not ROUGE_AVAILABLE:
            print("⚠️  ROUGE not available. Skipping generation evaluation.")
            return {}

        rouge_scores = {"rouge1": [], "rouge2": [], "rougeL": []}
        predictions = []
        references = []

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
                chunk_texts, _ = self.retrieve_chunks(question, k=2)
                context = "\n".join(chunk_texts)

                # Generate answer
                print(f"\n[{sample_count + 1}/{num_samples}] Generating answer...")
                print(f"  Question: {question[:60]}...")

                start_time = time.time()
                generated_answer = generate_answer(context, question, max_new_tokens=100)
                generation_time = time.time() - start_time

                print(f"  Generated in {generation_time:.2f}s")

                # Store for BERTScore
                predictions.append(generated_answer)
                references.append(reference_answer)

                # Calculate ROUGE scores
                if self.rouge_scorer:
                    scores = self.rouge_scorer.score(reference_answer, generated_answer)
                    rouge_scores["rouge1"].append(scores["rouge1"].fmeasure)
                    rouge_scores["rouge2"].append(scores["rouge2"].fmeasure)
                    rouge_scores["rougeL"].append(scores["rougeL"].fmeasure)

                sample_count += 1

        # Calculate average ROUGE scores
        metrics = {
            "rouge1": np.mean(rouge_scores["rouge1"]) if rouge_scores["rouge1"] else 0,
            "rouge2": np.mean(rouge_scores["rouge2"]) if rouge_scores["rouge2"] else 0,
            "rougeL": np.mean(rouge_scores["rougeL"]) if rouge_scores["rougeL"] else 0,
        }

        print("\n" + "-" * 70)
        print("ROUGE SCORES:")
        print(f"  ROUGE-1: {metrics['rouge1']:.4f}")
        print(f"  ROUGE-2: {metrics['rouge2']:.4f}")
        print(f"  ROUGE-L: {metrics['rougeL']:.4f}")

        # Calculate BERTScore if available
        if BERTSCORE_AVAILABLE and predictions:
            print("\nCalculating BERTScore (this may take a moment)...")
            try:
                P, R, F1 = bert_score(predictions, references, lang="en", verbose=False)
                metrics["bertscore_precision"] = P.mean().item()
                metrics["bertscore_recall"] = R.mean().item()
                metrics["bertscore_f1"] = F1.mean().item()

                print("\nBERTSCORE:")
                print(f"  Precision: {metrics['bertscore_precision']:.4f}")
                print(f"  Recall:    {metrics['bertscore_recall']:.4f}")
                print(f"  F1:        {metrics['bertscore_f1']:.4f}")
            except Exception as e:
                print(f"⚠️  BERTScore calculation failed: {e}")

        return metrics

    def run_full_evaluation(self, retrieval_samples: int = 50, generation_samples: int = 20):
        """
        Run complete evaluation pipeline.

        Args:
            retrieval_samples: Number of samples for retrieval evaluation
            generation_samples: Number of samples for generation evaluation
        """
        start_time = time.time()

        # Evaluate retrieval
        retrieval_metrics = self.evaluate_retrieval_performance(retrieval_samples)

        # Evaluate generation
        generation_metrics = self.evaluate_generation_quality(generation_samples)

        total_time = time.time() - start_time

        # Print final summary
        print("\n" + "=" * 70)
        print("FINAL EVALUATION SUMMARY")
        print("=" * 70)

        print("\n📊 RETRIEVAL METRICS:")
        print(f"  Precision@2: {retrieval_metrics.get('precision@2', 0):.4f}")
        print(f"  Recall@2:    {retrieval_metrics.get('recall@2', 0):.4f}")
        print(f"  MRR:         {retrieval_metrics.get('mrr', 0):.4f}")

        if generation_metrics:
            print("\n📝 GENERATION METRICS:")
            print(f"  ROUGE-1:     {generation_metrics.get('rouge1', 0):.4f}")
            print(f"  ROUGE-2:     {generation_metrics.get('rouge2', 0):.4f}")
            print(f"  ROUGE-L:     {generation_metrics.get('rougeL', 0):.4f}")

            if 'bertscore_f1' in generation_metrics:
                print(f"\n  BERTScore Precision: {generation_metrics.get('bertscore_precision', 0):.4f}")
                print(f"  BERTScore Recall:    {generation_metrics.get('bertscore_recall', 0):.4f}")
                print(f"  BERTScore F1:        {generation_metrics.get('bertscore_f1', 0):.4f}")

        print(f"\n⏱️  Total evaluation time: {total_time:.2f} seconds")
        print("=" * 70)

        # Save results to JSON
        results = {
            "retrieval": retrieval_metrics,
            "generation": generation_metrics,
            "metadata": {
                "retrieval_samples": retrieval_samples,
                "generation_samples": generation_samples,
                "total_time_seconds": total_time,
                "dataset": str(self.dataset_path)
            }
        }

        output_path = Path("evaluation_results.json")
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Results saved to: {output_path}")

        return results


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate RAG system performance")
    parser.add_argument("--retrieval_samples", type=int, default=50,
                       help="Number of samples for retrieval evaluation (default: 50)")
    parser.add_argument("--generation_samples", type=int, default=20,
                       help="Number of samples for generation evaluation (default: 20)")
    parser.add_argument("--dataset", type=str, default="dataset/tatqa_dataset_dev.json",
                       help="Path to TAT-QA dataset file")

    args = parser.parse_args()

    try:
        evaluator = RAGEvaluator(dataset_path=args.dataset)
        evaluator.run_full_evaluation(
            retrieval_samples=args.retrieval_samples,
            generation_samples=args.generation_samples
        )
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
