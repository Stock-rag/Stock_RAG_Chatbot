#!/bin/bash

################################################################################
# RAG System Evaluation Runner Script
################################################################################
#
# This script runs a comprehensive evaluation of the RAG system including:
# - Retrieval quality metrics (Precision@k, Recall@k, MRR)
# - Generation quality metrics (ROUGE, BERTScore)
#
# Usage:
#   ./run_evaluation.sh [retrieval_samples] [generation_samples]
#
# Examples:
#   ./run_evaluation.sh              # Use defaults (50 retrieval, 20 generation)
#   ./run_evaluation.sh 100 30       # Custom sample sizes
#
################################################################################

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "========================================================================"
echo "                   RAG SYSTEM EVALUATION RUNNER"
echo "========================================================================"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
RAGAPP_DIR="$SCRIPT_DIR/ragapp"

# Parse arguments
RETRIEVAL_SAMPLES=${1:-50}
GENERATION_SAMPLES=${2:-20}

echo ""
echo "Configuration:"
echo "  Retrieval samples:  $RETRIEVAL_SAMPLES"
echo "  Generation samples: $GENERATION_SAMPLES"
echo "  Working directory:  $RAGAPP_DIR"
echo ""

# Check if ragapp directory exists
if [ ! -d "$RAGAPP_DIR" ]; then
    echo -e "${RED}Error: ragapp directory not found at $RAGAPP_DIR${NC}"
    exit 1
fi

cd "$RAGAPP_DIR"

# Step 1: Check Python virtual environment
echo "========================================================================"
echo "Step 1: Checking Python environment"
echo "========================================================================"

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Step 2: Install dependencies
echo ""
echo "========================================================================"
echo "Step 2: Installing evaluation dependencies"
echo "========================================================================"

echo "Installing required packages..."
pip install -q rouge-score bert-score 2>&1 | grep -v "already satisfied" || true
echo -e "${GREEN}✓ Evaluation dependencies installed${NC}"

# Step 3: Check ChromaDB
echo ""
echo "========================================================================"
echo "Step 3: Checking ChromaDB"
echo "========================================================================"

if [ ! -d "chroma_db" ]; then
    echo -e "${YELLOW}ChromaDB not found. You need to run the embedder first.${NC}"
    echo "Run: python -c \"from embeder import embedder; embedder()\""
    echo ""
    read -p "Would you like to create the database now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating ChromaDB database..."
        python -c "from embeder import embedder; embedder()"
        echo -e "${GREEN}✓ Database created${NC}"
    else
        echo -e "${RED}Cannot proceed without database. Exiting.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ ChromaDB found${NC}"
fi

# Step 4: Run evaluation
echo ""
echo "========================================================================"
echo "Step 4: Running evaluation"
echo "========================================================================"
echo ""
echo -e "${YELLOW}⚠️  Note: This may take 10-30 minutes depending on sample size${NC}"
echo -e "${YELLOW}   Retrieval evaluation: ~1-2 minutes${NC}"
echo -e "${YELLOW}   Generation evaluation: ~5-15 seconds per sample${NC}"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

echo ""
echo "Starting evaluation..."
echo ""

python run_full_evaluation.py \
    --retrieval_samples "$RETRIEVAL_SAMPLES" \
    --generation_samples "$GENERATION_SAMPLES"

EXIT_CODE=$?

# Step 5: Display results
echo ""
echo "========================================================================"
echo "Evaluation Complete"
echo "========================================================================"

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Evaluation completed successfully!${NC}"
    echo ""
    echo "Results saved to: evaluation_results.json"
    echo ""

    if [ -f "evaluation_results.json" ]; then
        echo "Quick summary:"
        echo "----------------------------------------"
        python3 << 'EOF'
import json
try:
    with open('evaluation_results.json', 'r') as f:
        results = json.load(f)

    print("\n📊 RETRIEVAL METRICS:")
    ret = results.get('retrieval', {})
    print(f"  Precision@2: {ret.get('precision@2', 0):.4f}")
    print(f"  Recall@2:    {ret.get('recall@2', 0):.4f}")
    print(f"  MRR:         {ret.get('mrr', 0):.4f}")

    gen = results.get('generation', {})
    if gen:
        print("\n📝 GENERATION METRICS:")
        print(f"  ROUGE-1: {gen.get('rouge1', 0):.4f}")
        print(f"  ROUGE-2: {gen.get('rouge2', 0):.4f}")
        print(f"  ROUGE-L: {gen.get('rougeL', 0):.4f}")

        if 'bertscore_f1' in gen:
            print(f"\n  BERTScore F1: {gen.get('bertscore_f1', 0):.4f}")
except Exception as e:
    print(f"Could not parse results: {e}")
EOF
        echo "----------------------------------------"
    fi

    echo ""
    echo "You can view the full results with:"
    echo "  cat evaluation_results.json | python -m json.tool"
else
    echo -e "${RED}✗ Evaluation failed with exit code: $EXIT_CODE${NC}"
    exit $EXIT_CODE
fi

echo ""
echo "========================================================================"
