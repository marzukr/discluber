/*
    ./webpack.config.js
*/
const path = require('path');
module.exports = {
  entry: './app/components/App.js',
  output: {
    path: path.resolve('app/static/js'),
    filename: 'App_bundle.js'
  },
  module: {
    loaders: [
      { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.jsx$/, loader: 'babel-loader', exclude: /node_modules/ }
    ]
  }
}