const { defineConfig } = require('@vue/cli-service');
const dotenv = require('dotenv');
const os = require('os');

// 确保加载 .env 文件
dotenv.config();

// Log network interfaces for debugging
console.log('Network Interfaces:', os.networkInterfaces());

module.exports = defineConfig({
    devServer: {
      // Bug 修复：将代理配置为环境变量中定义的 API 基础 URL
      port: 8001, // 指定端口为 8001
      host: '0.0.0.0', // 允许外部访问
      allowedHosts: 'all', // Changed from array to string
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
      proxy: {
        '/xiaozhi-esp32-api': {
          target: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8002', // 后端 API 的基础 URL
          changeOrigin: true, // 允许跨域
        },
      },
      client: {
        webSocketURL: 'auto://0.0.0.0:0/ws', // Add this line
        overlay: false,
        logging: 'info',
      },
    },
});
