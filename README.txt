================================================================================
                    RAG CHATBOT - SETUP AND USAGE GUIDE
================================================================================

PROJECT NAME: RAG-ragfull
DESCRIPTION: Retrieval-Augmented Generation (RAG) Chatbot System
AUTHOR: AI-Powered Question Answering System
DATASET: TATQA (Table and Text Question Answering)

================================================================================
                            TABLE OF CONTENTS
================================================================================

1. What is This Project?
2. System Requirements
3. Quick Start Guide
4. Detailed Setup Instructions
5. How to Run the Chatbot
6. Testing the System
7. Troubleshooting Common Issues
8. Project Structure
9. Technical Details
10. API Documentation

================================================================================
                        1. WHAT IS THIS PROJECT?
================================================================================

This is a RAG (Retrieval-Augmented Generation) chatbot that:

- Answers questions using AI and semantic search
- Retrieves relevant information from a knowledge base (TATQA dataset)
- Generates accurate answers using a language model (LFM2-1.2B-RAG)
- Provides a web-based chat interface for easy interaction

HOW IT WORKS:
1. User asks a question
2. System finds relevant text chunks using semantic search (ChromaDB)
3. AI model generates an answer based on the retrieved context
4. Answer is displayed in the chat interface

================================================================================
                        2. SYSTEM REQUIREMENTS
================================================================================

REQUIRED SOFTWARE:
- Python 3.8 or higher
- Node.js 16 or higher
- pip (Python package manager)
- npm (Node package manager)

DISK SPACE:
- ~3.5 GB for models and dependencies

INTERNET:
- Required for initial model download
- After setup, can work offline

OPERATING SYSTEM:
- macOS (tested)
- Linux (should work)
- Windows (may need path adjustments)

================================================================================
                        3. QUICK START GUIDE
================================================================================

STEP 1: Open Terminal and navigate to project directory
--------
cd /path/to/RAG-ragfull

STEP 2: Start the Backend Server (Terminal 1)
--------
./run_backend.sh

WAIT for these messages:
- " Model loaded successfully!"
- "INFO:     Application startup complete."

This takes 10-15 minutes on FIRST RUN (downloading models)
Subsequent runs take ~30 seconds

STEP 3: Start the Frontend (Terminal 2 - NEW TERMINAL)
--------
./run_frontend.sh

WAIT for:
- "�  Local:   http://localhost:5173/"

STEP 4: Open Browser
--------
Navigate to: http://localhost:5173

STEP 5: Start Chatting!
--------
Type a question and press Enter

================================================================================
                    4. DETAILED SETUP INSTRUCTIONS
================================================================================

FIRST TIME SETUP:

A. Install Python Dependencies
   ----------------------------
   cd /path/to/RAG-ragfull/ragapp

   pip install fastapi uvicorn transformers torch sentence-transformers chromadb nltk

   OR use the requirements file:
   pip install -r pythonserver/requirements.txt

B. Install Frontend Dependencies (Optional - script does this)
   ----------------------------
   cd /path/to/RAG-ragfull/ragapp/client
   npm install

C. Create Vector Database (Automatic on first run)
   ----------------------------
   The startup script automatically creates the ChromaDB database.

   To manually create it:
   cd /path/to/RAG-ragfull/ragapp
   python -c "from embeder import embedder; embedder()"

D. Download Language Model (Automatic on first run)
   ----------------------------
   The LFM2-1.2B-RAG model (~2.3GB) downloads automatically
   It's cached in: ~/.cache/huggingface/

================================================================================
                        5. HOW TO RUN THE CHATBOT
================================================================================

OPTION 1: Using Shell Scripts (Easiest)
----------------------------------------

Terminal 1 - Backend:
cd /path/to/RAG-ragfull
./run_backend.sh

Terminal 2 - Frontend:
cd /path/to/RAG-ragfull
./run_frontend.sh

Browser:
Open http://localhost:5173


OPTION 2: Manual Start
----------------------------------------

Terminal 1 - Backend:
cd /path/to/RAG-ragfull/ragapp
source venv/bin/activate
uvicorn pythonserver.main:app --reload --host 0.0.0.0 --port 8000

Terminal 2 - Frontend:
cd /path/to/RAG-ragfull/ragapp/client
npm run dev

Browser:
Open http://localhost:5173


STOPPING THE SERVERS:
----------------------------------------
Press Ctrl+C in each terminal window

================================================================================
                        6. TESTING THE SYSTEM
================================================================================

TEST 1: Check Backend Health
-----------------------------
Open browser: http://localhost:8000
Expected output: {"message":"RAG API running!"}

TEST 2: View API Documentation
-------------------------------
Open browser: http://localhost:8000/docs
You'll see interactive API documentation (Swagger UI)

TEST 3: Test API Directly
--------------------------
Open a new terminal and run:

curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is revenue?"}'

Expected output: JSON with "context" and "answer" fields

TEST 4: Use Frontend Chat Interface
------------------------------------
1. Open http://localhost:5173
2. Type a question: "What is the company revenue?"
3. Press Enter
4. Wait for AI-generated response

TEST 5: Run Component Tests (Optional)
---------------------------------------
cd /Users/brijeshmuralikrishnan/Downloads/RAG-ragfull/ragapp
python test_setup.py

This tests:
- Embedding model loading
- ChromaDB connection
- LLM model loading (optional)

================================================================================
                    7. TROUBLESHOOTING COMMON ISSUES
================================================================================

ISSUE 1: Port Already in Use
-----------------------------
ERROR: "Address already in use"

SOLUTION:
Kill the process using the port:
lsof -ti:8000 | xargs kill -9   # For backend
lsof -ti:5173 | xargs kill -9   # For frontend

Or use different ports:
uvicorn pythonserver.main:app --port 8001
npm run dev -- --port 5174


ISSUE 2: Module Not Found
--------------------------
ERROR: "ModuleNotFoundError: No module named 'xxx'"

SOLUTION:
Activate virtual environment and install:
cd /path/to/RAG-ragfull/ragapp
source venv/bin/activate
pip install fastapi uvicorn transformers torch sentence-transformers chromadb nltk


ISSUE 3: ChromaDB Collection Not Found
---------------------------------------
ERROR: "Collection not found"

SOLUTION:
Run the embedder to create the database:
cd /path/to/RAG-ragfull/ragapp
python -c "from embeder import embedder; embedder()"


ISSUE 4: Model Download Failed
-------------------------------
ERROR: "Failed to download model"

SOLUTION:
- Check internet connection
- Retry - downloads resume from where they stopped
- Manually check cache: ls ~/.cache/huggingface/


ISSUE 5: Slow Response Times
-----------------------------
SYMPTOMS: Answers take 5+ seconds

EXPECTED BEHAVIOR:
- First query: 5-10 seconds (model warmup)
- Subsequent queries: 2-5 seconds on CPU

SOLUTION (if too slow):
- This is normal on CPU
- For faster responses, use a GPU-enabled system
- Reduce max_new_tokens in llm/model_load.py


ISSUE 6: CORS Errors in Browser
--------------------------------
ERROR: "Access to XMLHttpRequest blocked by CORS"

SOLUTION:
Ensure backend is running on port 8000
Check pythonserver/main.py has CORS enabled (should be by default)


ISSUE 7: Frontend Not Loading
------------------------------
ERROR: "Cannot GET /"

SOLUTION:
1. Check if frontend dev server is running
2. Verify URL is http://localhost:5173 (not 8000)
3. Check terminal for frontend errors
4. Try: cd ragapp/client && npm install && npm run dev

================================================================================
                        8. PROJECT STRUCTURE
================================================================================

RAG-ragfull/

   README.md                   # Project overview (Markdown format)
   README.txt                  # This file
   SETUP_GUIDE.md             # Detailed setup instructions
   run_backend.sh             # Backend startup script
   run_frontend.sh            # Frontend startup script

   ragapp/
    
       pythonserver/          # FastAPI Backend
          main.py           # FastAPI app entry point
          controllers/      # Business logic
             rag_controller.py
          routes/           # API endpoints
              rag_routes.py
    
       data/                  # Data Processing
          loader.py         # Load JSON datasets
          chunker.py        # Split text into chunks
          prepare_data.py   # Transform data structure
    
       model/                 # Embedding Models
          embedding_model.py # SentenceTransformers loader
    
       llm/                   # Language Models
          model_load.py     # LLM loading & inference
          model_save.py     # Model download script
    
       retriever/             # Retrieval Logic
          chroma_retriever.py # Vector search
    
       vectorstore/           # Vector Database
          chroma_manager.py  # ChromaDB operations
    
       evaluation/            # Metrics & Evaluation
          evaluate.py       # Evaluation pipeline
          metrics.py        # Precision, Recall, MRR
    
       client/                # React Frontend
          src/
             api.js        # Axios HTTP client
          package.json
          README.md
    
       server/                # Node.js Server (Optional)
          server.js         # Express app
          src/
              routes/
              controllers/
    
       dataset/               # TATQA Dataset
          tatqa_dataset_train.json
          tatqa_dataset_dev.json
          tatqa_dataset_test.json
          tatqa_dataset_test_gold.json
    
       chroma_db/             # Vector Database Storage (Created on first run)
       venv/                  # Python Virtual Environment (Created on first run)
       embeder.py             # Data Ingestion Pipeline
       test_setup.py          # System Test Script

================================================================================
                        9. TECHNICAL DETAILS
================================================================================

BACKEND ARCHITECTURE:
---------------------
Framework: FastAPI (Python)
Server: Uvicorn (ASGI)
Port: 8000

MODELS:
-------
1. Embedding Model:
   - Name: all-MiniLM-L6-v2
   - Type: SentenceTransformers
   - Output: 384-dimensional embeddings
   - Size: ~90MB
   - Purpose: Convert text to vectors for semantic search

2. Language Model:
   - Name: LiquidAI/LFM2-1.2B-RAG
   - Type: Causal Language Model
   - Size: ~2.3GB
   - Parameters: 1.2 billion
   - Purpose: Generate answers based on context

VECTOR DATABASE:
----------------
Database: ChromaDB
Storage: Persistent (./chroma_db)
Collection: finance_docs
Similarity: Cosine similarity
Top-K Retrieval: 5 results, return top 2

FRONTEND:
---------
Framework: React 18
Build Tool: Vite
HTTP Client: Axios
Styling: TailwindCSS
Port: 5173

DATA PROCESSING:
----------------
Dataset: TATQA (Table and Text QA)
Chunk Size: 100 tokens
Tokenizer: NLTK punkt
Question Type: Text-only (filtered)

EVALUATION METRICS:
-------------------
- Precision@k
- Recall@k
- Mean Reciprocal Rank (MRR)

================================================================================
                        10. API DOCUMENTATION
================================================================================

BASE URL: http://localhost:8000

ENDPOINTS:

1. Health Check
   ------------
   GET /

   Response:
   {
     "message": "RAG API running!"
   }

2. Generate Answer
   ---------------
   POST /api/generate

   Request Body:
   {
     "query": "Your question here"
   }

   Response:
   {
     "context": "Retrieved text chunks...",
     "answer": "Generated answer..."
   }

   Example:
   curl -X POST "http://localhost:8000/api/generate" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the revenue?"}'

3. Interactive API Docs
   --------------------
   GET /docs

   Opens Swagger UI for interactive API testing

4. Alternative API Docs
   --------------------
   GET /redoc

   Opens ReDoc documentation

================================================================================
                        EXAMPLE USAGE SCENARIOS
================================================================================

SCENARIO 1: Ask About Revenue
------------------------------
Question: "What is the company's revenue?"
System: Searches for revenue-related chunks � Generates answer
Expected: Detailed answer with revenue figures from dataset

SCENARIO 2: Financial Metrics
------------------------------
Question: "What was the profit margin in Q1?"
System: Retrieves Q1 financial data � Generates answer
Expected: Answer with specific profit margin percentages

SCENARIO 3: Comparative Questions
----------------------------------
Question: "How did revenue change from 2022 to 2023?"
System: Finds relevant years � Compares data � Generates answer
Expected: Year-over-year comparison with percentages

================================================================================
                        PERFORMANCE BENCHMARKS
================================================================================

FIRST RUN:
- Model download: 5-10 minutes (one-time)
- Database creation: 2-5 minutes (one-time)
- Server startup: 30-60 seconds

SUBSEQUENT RUNS:
- Server startup: 10-30 seconds
- First query: 5-10 seconds (model warmup)
- Follow-up queries: 2-5 seconds (CPU)

RESOURCE USAGE:
- RAM: ~4GB (models loaded in memory)
- CPU: 100% during inference (2-5 seconds)
- Disk: ~3.5GB total

================================================================================
                        DEVELOPMENT & CUSTOMIZATION
================================================================================

MODIFY RETRIEVAL:
Edit: ragapp/retriever/chroma_retriever.py
- Change n_results to retrieve more/fewer chunks
- Adjust filtering logic

MODIFY LLM GENERATION:
Edit: ragapp/llm/model_load.py
- Change max_new_tokens for longer/shorter answers
- Modify prompt template
- Adjust temperature (add to generate() call)

CHANGE EMBEDDING MODEL:
Edit: ragapp/model/embedding_model.py
- Change model_name parameter
- Options: all-mpnet-base-v2, paraphrase-MiniLM-L6-v2

ADD NEW API ENDPOINTS:
Edit: ragapp/pythonserver/routes/rag_routes.py
- Add new route decorators
- Implement in controllers/

CUSTOMIZE FRONTEND:
Edit: ragapp/client/src/
- Modify React components
- Update styling
- Add new features

================================================================================
                        IMPORTANT NOTES
================================================================================

1. FIRST RUN TAKES TIME:
   - Be patient during initial model download (~2.3GB)
   - Downloads are cached and only happen once

2. INTERNET REQUIRED:
   - First run: Download models
   - After setup: Can work offline

3. RESOURCE INTENSIVE:
   - Models use ~4GB RAM
   - CPU usage spikes during answer generation

4. DATASET SPECIFIC:
   - Answers are based on TATQA dataset
   - Won't answer questions outside this domain well

5. SECURITY:
   - CORS is set to allow all origins (*)
   - Change this in production!
   - Located in: pythonserver/main.py

6. HARDCODED PATHS FIXED:
   - Previous Windows paths (D:/) have been updated
   - Models now auto-download from Hugging Face

7. MODEL CACHING:
   - Models cached in: ~/.cache/huggingface/
   - To clear cache: rm -rf ~/.cache/huggingface/

8. UPDATES:
   - To update models: Delete cache and restart
   - To update code: Pull latest changes and restart

================================================================================
                        GETTING HELP
================================================================================

IF YOU ENCOUNTER ISSUES:

1. Check this README for troubleshooting
2. Check SETUP_GUIDE.md for detailed instructions
3. View terminal logs for error messages
4. Check browser console (F12) for frontend errors
5. Test components individually using test_setup.py

COMMON COMMANDS:

- Check Python version: python --version
- Check Node version: node --version
- List running processes: ps aux | grep python
- Check port usage: lsof -i :8000
- View logs: Check terminal output
- Clear cache: rm -rf ~/.cache/huggingface/

================================================================================
                        QUICK REFERENCE
================================================================================

START BACKEND:
cd /path/to/RAG-ragfull
./run_backend.sh

START FRONTEND:
cd /path/to/RAG-ragfull
./run_frontend.sh

STOP SERVERS:
Press Ctrl+C in each terminal

ACCESS CHATBOT:
http://localhost:5173

ACCESS API DOCS:
http://localhost:8000/docs

TEST API:
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"query": "test question"}'

RUN TESTS:
cd ragapp
python test_setup.py

CREATE DATABASE:
cd ragapp
python -c "from embeder import embedder; embedder()"

================================================================================
                        VERSION INFORMATION
================================================================================

Project Version: 1.0.0
Last Updated: 2025
Python Version Required: 3.8+
Node.js Version Required: 16+

Key Dependencies:
- fastapi: Web framework
- uvicorn: ASGI server
- transformers: HuggingFace models
- torch: PyTorch framework
- sentence-transformers: Embedding models
- chromadb: Vector database
- nltk: Natural language processing
- react: Frontend framework
- vite: Build tool
- axios: HTTP client

================================================================================
                        LICENSE & CREDITS
================================================================================

Dataset: TATQA (Table and Text Question Answering)
Models:
- LiquidAI/LFM2-1.2B-RAG
- sentence-transformers/all-MiniLM-L6-v2

Technologies:
- FastAPI
- React
- ChromaDB
- PyTorch
- Transformers (HuggingFace)

================================================================================
                        END OF README
================================================================================

For more detailed information, see:
- SETUP_GUIDE.md - Complete setup instructions
- README.md - Project overview in Markdown format

For code documentation, all Python and JavaScript files include
comprehensive docstrings and comments.

Happy chatting with your RAG bot! >
