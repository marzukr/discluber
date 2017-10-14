/*
    ./webpack.config.js
*/
const webpack = require("webpack");
const path = require("path");
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: {
        app: "./app/components/App.js",
    },
    output: {
        path: path.resolve("app/static/js"),
        filename: "[name]_bundle.js"
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                loader: "babel-loader",
                exclude: /node_modules/
            },
            {
                test: /\.jsx$/,
                loader: "babel-loader",
                exclude: /node_modules/
            },
            {
                test: /\.(scss)$/,
                loader: ExtractTextPlugin.extract("css-loader!postcss-loader!sass-loader"),
            },
        ],
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            Popper: ['popper.js', 'default'],
        }),
        new ExtractTextPlugin("../css/[name].css", {
            allChunks: true,
        }),
    ],
};