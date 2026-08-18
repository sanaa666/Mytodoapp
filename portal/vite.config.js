import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/Mytodoapp/',
  server: {
    proxy: {
      '/users': 'https://sanaa666.github.io/Mytodoapp/',
      '/login': 'https://sanaa666.github.io/Mytodoapp/',
      '/todos': 'https://sanaa666.github.io/Mytodoapp/',

    },
  },
})
