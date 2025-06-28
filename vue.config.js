module.exports = {
  publicPath: './',
  css: {
    loaderOptions: {
      less: {
        javascriptEnabled: true
      }
    }
  },
  lintOnSave: false,
  devServer: {
    proxy: {
      '/api': {  // 代理所有以 `/api` 开头的请求
        target: 'http://localhost:8080', // 替换为实际后端地址（如 http://localhost:3000）
        changeOrigin: true, // 允许跨域
        pathRewrite: {
          '^/api': '' // 移除请求路径中的 `/api` 前缀（按需调整）
        }
      }
    }
  }
}
