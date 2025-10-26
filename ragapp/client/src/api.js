/**
 * API client configuration for RAG application frontend.
 *
 * This module sets up an Axios instance with configured base URL and headers
 * for making HTTP requests to the backend API. It supports environment-based
 * configuration for different deployment environments.
 *
 * @module api
 */

import axios from 'axios'

/**
 * Base URL for API requests.
 *
 * Configured via VITE_API_URL environment variable in .env file.
 * Falls back to localhost:5000 for local development.
 *
 * @type {string}
 * @example
 * // In .env file:
 * // VITE_API_URL=http://localhost:5000
 * // VITE_API_URL=https://api.production.com
 */
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

/**
 * Configured Axios instance for API requests.
 *
 * Pre-configured with:
 * - Base URL from environment or localhost
 * - JSON content-type header
 *
 * @type {import('axios').AxiosInstance}
 * @example
 * import api from './api'
 *
 * // Make a POST request to generate answer
 * const response = await api.post('/api/generate', { query: 'What is revenue?' })
 * console.log(response.data.answer)
 */
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default api
