import { defineConfig } from 'vite'; // Standard Vite defineConfig
import vue from '@vitejs/plugin-vue';
// For Vitest configuration, we can augment the existing Vite config.
// No separate defineVitestConfig is strictly needed if merging into Vite's defineConfig.
import fs from 'fs';
import path from 'path'

const ipAddress = '192.168.68.102';

export default defineConfig({
  plugins: [vue()],
  // Vitest configuration
  test: {
    globals: true, // to use Vitest globals like describe, it, expect without importing
    environment: 'happy-dom', // Use happy-dom for a browser-like environment
    setupFiles: [], // Optional: if you need setup files
  },
  server: {
    host: '0.0.0.0', 
    port: 5173,
    https: {
      key: fs.readFileSync(path.resolve(__dirname, `${ipAddress}-key.pem`)),
      cert: fs.readFileSync(path.resolve(__dirname, `${ipAddress}.pem`)),
    },
  }
})