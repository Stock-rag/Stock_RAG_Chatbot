/**
 * Express.js backend server for RAG application.
 *
 * This is an alternative backend implementation using Node.js/Express
 * that proxies requests to the Python-based RAG system. It provides
 * a REST API for the frontend client.
 *
 * @module server
 */

import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import chatRoutes from "./src/routes/chatRoutes.js";

// Load environment variables from .env file
dotenv.config();

// Initialize Express application
const app = express();

// Middleware: Parse JSON request bodies
app.use(express.json());

// Middleware: Enable CORS for cross-origin requests from frontend
app.use(cors());

// Routes: Register RAG API routes under /api/rag prefix
app.use("/api/rag", chatRoutes);

// Start server on configured port
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
