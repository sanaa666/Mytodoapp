import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/users': 'http://127.0.0.1:8000',
      '/users': 'https://sanaa666.github.io/Mytodoapp/',
      '/login': 'http://127.0.0.1:8000',
      '/login': 'https://sanaa666.github.io/Mytodoapp/',
      '/todos': 'http://127.0.0.1:8000',
      '/todos': 'https://sanaa666.github.io/Mytodoapp/',

    },
  },
})
