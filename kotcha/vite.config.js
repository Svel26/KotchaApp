import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

const ipAddress = '192.168.68.102';

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', 
    port: 5173,
    https: {
      key: fs.readFileSync(path.resolve(__dirname, `${ipAddress}-key.pem`)),
      cert: fs.readFileSync(path.resolve(__dirname, `${ipAddress}.pem`)),
    },
  }
})