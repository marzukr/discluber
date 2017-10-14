const merge = require('webpack-merge');
const common = require('./webpack.common.js');

const ExtractTextPlugin = require("extract-text-webpack-plugin");
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

module.exports = merge(common, {
    module: {
        loaders: [
            {
                test: /\.(scss)$/,
                loader: ExtractTextPlugin.extract([
                    {
                        loader: "css-loader",
                        options: {
                            minimize: true,
                        }
                    },
                    {
                        loader: "postcss-loader",
                    },
                    {
                        loader: "sass-loader",
                    },
                ]),
            },
        ],
    },
    plugins: [
        new ExtractTextPlugin("../css/[name].css", {
            allChunks: true,
        }),
        new UglifyJSPlugin(),
    ],
});