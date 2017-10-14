const merge = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    module: {
        loaders: [
            {
                test: /\.(scss)$/,
                use: ["style-loader", "css-loader", "postcss-loader", "sass-loader"],
            },
        ],
    }
});