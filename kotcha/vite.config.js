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

    // Enable HTTPS with the certificates you generated
    https: {
      key: fs.readFileSync(path.resolve(__dirname, 'localhost-key.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, 'localhost.pem')),
    },

    // IMPORTANT: You will need to add your ngrok URL here later
    allowedHosts: [
      "https://9ca6-77-171-218-237.ngrok-free.app/"
    ],
  }
})