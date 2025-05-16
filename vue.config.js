module.exports = {
  publicPath: "./",
  css: {
    loaderOptions: {
      less: {
        javascriptEnabled: true,
      },
    },
  },
  lintOnSave: false,
  transpileDependencies: ["chart.js"],
};
