module.exports = {
  outputDir: "../server/dist",
  assetsDir: "static" ,
  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      rtlSupport: true
    }
  },
  transpileDependencies: [
    'quasar'
  ],
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title = "PID Controller"
        return args
      })
  }
}
