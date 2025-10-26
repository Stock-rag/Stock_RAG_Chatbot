# RAG System Evaluation Guide

This guide explains how to evaluate your RAG chatbot and generate the metrics needed for your WIL project report.

## Quick Start

### Option 1: Using the Shell Script (Easiest)

```bash
cd /path/to/RAG-ragfull
./run_evaluation.sh
```

This will:
1. Check your Python environment
2. Install evaluation dependencies (rouge-score, bert-score)
3. Verify ChromaDB is populated
4. Run comprehensive evaluation
5. Save results to `evaluation_results.json`

### Option 2: Manual Execution

```bash
cd /path/to/RAG-ragfull/ragapp

# Activate virtual environment
source venv/bin/activate

# Install evaluation libraries
pip install rouge-score bert-score

# Run evaluation
python run_full_evaluation.py --retrieval_samples 50 --generation_samples 20
```

## Evaluation Parameters

### `--retrieval_samples` (default: 50)
Number of questions to use for evaluating retrieval quality (Precision@k, Recall@k, MRR).

**Recommendation:** Use 50-100 for balance between accuracy and speed.

### `--generation_samples` (default: 20)
Number of questions to use for evaluating generation quality (ROUGE, BERTScore).

**Recommendation:** Use 20-30 samples. Generation is slow (~5-15 seconds per sample).

### Example with custom parameters:
```bash
python run_full_evaluation.py --retrieval_samples 100 --generation_samples 30
```

## What Gets Evaluated?

### 1. Retrieval Quality Metrics

**Precision@2**
- Measures: What fraction of retrieved chunks are relevant?
- Range: 0.0 (worst) to 1.0 (best)
- Interpretation: 0.75 means 75% of retrieved chunks were actually relevant

**Recall@2**
- Measures: What fraction of relevant chunks were retrieved?
- Range: 0.0 (worst) to 1.0 (best)
- Interpretation: 0.60 means the system found 60% of all relevant chunks

**MRR (Mean Reciprocal Rank)**
- Measures: How quickly does the system find the first relevant result?
- Range: 0.0 (worst) to 1.0 (best)
- Interpretation: 0.85 means the first relevant chunk appears very early in results

### 2. Generation Quality Metrics

**ROUGE-1**
- Measures: Unigram (single word) overlap between generated and reference answers
- Range: 0.0 (worst) to 1.0 (best)
- Interpretation: 0.45 means 45% of words match the reference

**ROUGE-2**
- Measures: Bigram (two-word phrase) overlap
- Range: 0.0 (worst) to 1.0 (best)
- Interpretation: Usually lower than ROUGE-1; measures phrase-level accuracy

**ROUGE-L**
- Measures: Longest common subsequence between answers
- Range: 0.0 (worst) to 1.0 (best)
- Interpretation: Captures sentence structure similarity

**BERTScore**
- Measures: Semantic similarity using contextual embeddings
- Components: Precision, Recall, F1
- Range: 0.0 (worst) to 1.0 (best)
- Interpretation: 0.85+ indicates strong semantic similarity, even if exact words differ

## Expected Results for Your Report

Based on typical RAG system performance, here are **estimated ranges** you might see:

### Retrieval Metrics
| Metric        | Expected Range | Good Performance |
|---------------|----------------|------------------|
| Precision@2   | 0.40 - 0.70    | ≥ 0.60          |
| Recall@2      | 0.30 - 0.60    | ≥ 0.50          |
| MRR           | 0.60 - 0.90    | ≥ 0.75          |

### Generation Metrics
| Metric              | Expected Range | Good Performance |
|---------------------|----------------|------------------|
| ROUGE-1             | 0.25 - 0.50    | ≥ 0.35          |
| ROUGE-2             | 0.10 - 0.30    | ≥ 0.20          |
| ROUGE-L             | 0.20 - 0.45    | ≥ 0.30          |
| BERTScore F1        | 0.70 - 0.90    | ≥ 0.80          |

**Note:** These are estimates. Your actual results will vary based on:
- Dataset quality (TAT-QA)
- Model performance (LFM2-1.2B-RAG)
- Retrieval strategy (ChromaDB with all-MiniLM-L6-v2)
- Chunk size and overlap

## Output Files

### `evaluation_results.json`
Contains complete evaluation results:

```json
{
  "retrieval": {
    "precision@2": 0.6234,
    "recall@2": 0.5123,
    "mrr": 0.7845
  },
  "generation": {
    "rouge1": 0.3856,
    "rouge2": 0.2145,
    "rougeL": 0.3421,
    "bertscore_precision": 0.8234,
    "bertscore_recall": 0.8156,
    "bertscore_f1": 0.8195
  },
  "metadata": {
    "retrieval_samples": 50,
    "generation_samples": 20,
    "total_time_seconds": 487.32,
    "dataset": "dataset/tatqa_dataset_dev.json"
  }
}
```

### Viewing Results

**Pretty-print JSON:**
```bash
cat ragapp/evaluation_results.json | python -m json.tool
```

**Extract specific metrics:**
```bash
# Get retrieval metrics
python3 -c "import json; r=json.load(open('ragapp/evaluation_results.json')); print('Precision@2:', r['retrieval']['precision@2'])"

# Get generation metrics
python3 -c "import json; r=json.load(open('ragapp/evaluation_results.json')); print('ROUGE-1:', r['generation']['rouge1'])"
```

## Using Results in Your Report

### For Section 4.2.1: Retrieval Performance

**Table: Retrieval Performance Metrics**

| Metric       | Score  |
|--------------|--------|
| Precision@2  | 0.6234 |
| Recall@2     | 0.5123 |
| MRR          | 0.7845 |

**Interpretation:**
> The retrieval component achieved a Precision@2 of 0.62, indicating that 62% of retrieved chunks were relevant to the query. The Recall@2 of 0.51 shows that the system successfully retrieved approximately half of all relevant chunks. The MRR of 0.78 demonstrates that relevant documents typically appear in the first or second position of results.

### For Section 4.2.2: Generation Quality

**Table: Answer Generation Quality**

| Metric              | Score  |
|---------------------|--------|
| ROUGE-1             | 0.3856 |
| ROUGE-2             | 0.2145 |
| ROUGE-L             | 0.3421 |
| BERTScore Precision | 0.8234 |
| BERTScore Recall    | 0.8156 |
| BERTScore F1        | 0.8195 |

**Interpretation:**
> The LFM2-1.2B-RAG model achieved a ROUGE-1 score of 0.39, indicating moderate lexical overlap with reference answers. The BERTScore F1 of 0.82 demonstrates strong semantic similarity, suggesting that while generated answers may use different wording, they capture the correct meaning. The lower ROUGE-2 score of 0.21 is expected, as exact phrase matching is more challenging in generative systems.

## Troubleshooting

### Error: "Collection not found"
**Solution:** Run the embedder first:
```bash
cd ragapp
python -c "from embeder import embedder; embedder()"
```

### Error: "Module not found: rouge_score"
**Solution:** Install evaluation dependencies:
```bash
pip install rouge-score bert-score
```

### Evaluation is too slow
**Solutions:**
1. Reduce sample sizes:
   ```bash
   python run_full_evaluation.py --retrieval_samples 30 --generation_samples 10
   ```
2. Skip BERTScore (comment out in code) - it's the slowest metric
3. Run overnight if evaluating on large sample

### BERTScore fails with memory error
**Solutions:**
1. Reduce `--generation_samples` to 10-15
2. BERTScore loads a BERT model (~500MB RAM)
3. Close other applications to free memory
4. You can still report ROUGE scores without BERTScore

## Time Estimates

| Task                        | Duration          |
|-----------------------------|-------------------|
| Environment setup           | 2-5 minutes       |
| Install dependencies        | 1-2 minutes       |
| Retrieval eval (50 samples) | 1-3 minutes       |
| Generation eval (20 samples)| 2-10 minutes      |
| **Total**                   | **6-20 minutes**  |

**Note:** Generation evaluation is CPU-intensive. First-time BERTScore download adds ~2 minutes.

## Advanced: Batch Processing

If you need to evaluate multiple configurations:

```bash
# Create a batch script
cat > batch_eval.sh << 'EOF'
#!/bin/bash
for samples in 25 50 100; do
    echo "Running with $samples samples..."
    python run_full_evaluation.py \
        --retrieval_samples $samples \
        --generation_samples 20
    mv evaluation_results.json "results_${samples}.json"
done
EOF

chmod +x batch_eval.sh
./batch_eval.sh
```

## Comparing Results

To compare different retrieval strategies or model configurations:

```python
import json

# Load multiple result files
with open('results_baseline.json') as f:
    baseline = json.load(f)

with open('results_optimized.json') as f:
    optimized = json.load(f)

# Compare
print("Precision@2 improvement:",
      optimized['retrieval']['precision@2'] - baseline['retrieval']['precision@2'])
```

## Questions?

If you encounter issues:
1. Check terminal output for error messages
2. Verify ChromaDB is populated: `ls -lh ragapp/chroma_db/`
3. Ensure models are loaded: Check for `~/.cache/huggingface/`
4. Review evaluation script logs in terminal

---

**For your WIL report:** Run the evaluation once with the default parameters (50 retrieval, 20 generation), then use those results throughout your Findings section. Make sure to mention:

1. **Sample size** used for evaluation
2. **Dataset** used (TAT-QA dev set)
3. **Evaluation methodology** (automated metrics)
4. **Interpretation** of results in context

Good luck with your project! 🚀
