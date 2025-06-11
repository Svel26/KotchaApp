import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  server: {
    // Host on all network interfaces to make it accessible
    host: '0.0.0.0', 
    port: 5173,

    // Enable HTTPS using the certificates you generated with mkcert
    https: {
      key: fs.readFileSync(path.resolve(__dirname, 'localhost-key.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, 'localhost.pem')),
    },

    // Allow ngrok to connect to the server
    allowedHosts: [
      '5956-77-171-218-237.ngrok-free.app'
    ],
  }
})