import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // Ensure this matches the port in docker-compose.yml
    host: '0.0.0.0', // Allow connections from outside the container
  },
})
