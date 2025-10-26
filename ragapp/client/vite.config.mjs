import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// optional: proxy to backend (adjust port if needed)
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:5000', // your Express server
    },
  },
})