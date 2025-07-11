// static/vite.config.js
import { defineConfig } from 'vite'

export default defineConfig({
  root: '.', // 保证以 static 目录为根
  server: {
    open: true, // 启动自动打开浏览器，可选
  },
})