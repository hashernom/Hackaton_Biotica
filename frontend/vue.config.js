const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    https: false,
    host: '0.0.0.0',
    port: 8081,
    hot: true,
    open: false,
    allowedHosts: 'all',
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
    },
    client: {
      webSocketURL: 'ws://0.0.0.0:8081/ws'
    },
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        ws: false
      }
    }
  },
  configureWebpack: {
    resolve: {
      fallback: { fs: false, path: false, http: false, https: false }
    }
  }
})