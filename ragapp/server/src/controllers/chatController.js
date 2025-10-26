/**
 * Chat controller for RAG application.
 *
 * This module handles chat and answer generation requests by spawning
 * Python processes to run the RAG model. It acts as a bridge between
 * the Node.js Express server and the Python-based ML models.
 *
 * @module controllers/chatController
 */

import { spawn } from "child_process";

/**
 * Generate answer using Python-based RAG model.
 *
 * This controller spawns a Python child process that runs the LLM to generate
 * an answer based on the provided context and query. It communicates with the
 * Python script via stdin/stdout using JSON.
 *
 * @param {Object} req - Express request object
 * @param {Object} req.body - Request body
 * @param {string} req.body.context - Retrieved context chunks
 * @param {string} req.body.query - User's question
 * @param {Object} res - Express response object
 *
 * @returns {Promise<void>}
 *
 * @example
 * POST /api/rag/query
 * {
 *   "context": "Revenue for Q1 was $1.2M...",
 *   "query": "What is the revenue?"
 * }
 *
 * Response:
 * {
 *   "answer": "The revenue for Q1 was $1.2 million..."
 * }
 *
 * Note:
 *   - Uses hardcoded Python script path: D:/RAG_APP/model/model_load.py
 *   - This path should be configurable via environment variables
 */
export const getAnswer = (req, res) => {
  const { context, query } = req.body;

  // Spawn Python process to run the LLM model
  // TODO: Make this path configurable via environment variables
  const python = spawn("python", ["D:/RAG_APP/model/model_load.py"]);

  // Send input data to Python script via stdin
  python.stdin.write(JSON.stringify({ context, query }));
  python.stdin.end();

  // Accumulate output data from Python process
  let data = "";

  // Listen for data from Python stdout
  python.stdout.on("data", (chunk) => {
    data += chunk.toString();
  });

  // Log any errors from Python stderr
  python.stderr.on("data", (err) => {
    console.error("Python error:", err.toString());
  });

  // Process results when Python process exits
  python.on("close", () => {
    try {
      // Parse JSON response from Python
      const result = JSON.parse(data);
      console.log(result);
      res.json({ answer: result.answer });
    } catch (e) {
      // Handle JSON parsing errors
      res.json({ error: e });
    }
  });
};

/**
 * Handle basic chat requests (placeholder implementation).
 *
 * This is a simple echo endpoint for testing purposes. In production,
 * this would be replaced with actual chat handling logic or removed.
 *
 * @param {Object} req - Express request object
 * @param {Object} req.body - Request body
 * @param {string} req.body.query - User's message
 * @param {Object} res - Express response object
 *
 * @returns {Promise<void>}
 *
 * @example
 * POST /api/rag/chat
 * {
 *   "query": "Hello"
 * }
 *
 * Response:
 * {
 *   "answer": "You said: Hello"
 * }
 */
export const handleChat = async (req, res) => {
  try {
    const { query } = req.body;

    // Placeholder response - echoes user input
    res.json({ answer: `You said: ${query}` });
  } catch (error) {
    console.error("Chat error:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};
