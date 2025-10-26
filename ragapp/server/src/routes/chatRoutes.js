/**
 * Chat/RAG routes for Express server.
 *
 * This module defines the REST API routes for handling chat and RAG queries.
 *
 * @module routes/chatRoutes
 */

import express from "express";
import { handleChat, getAnswer } from "../controllers/chatController.js";

// Create Express router
const router = express.Router();

/**
 * POST /query - Generate answer using RAG pipeline
 *
 * Request body:
 *   - context (string): Retrieved context chunks
 *   - query (string): User's question
 *
 * Response:
 *   - answer (string): Generated answer from LLM
 */
router.post("/query", getAnswer);

export default router;