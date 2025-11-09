import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// ✅ Add base and server proxy if needed
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
  },
  server: {
    port: 5173,
  },
})
  