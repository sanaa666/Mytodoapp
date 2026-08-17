import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/users': 'http://127.0.0.1:8000',
      '/login': 'http://127.0.0.1:8000',
      '/todos': 'http://127.0.0.1:8000',

    },
  },
})
