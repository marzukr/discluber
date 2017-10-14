/*
    ./webpack.config.js
*/
const webpack = require("webpack");
const path = require("path");

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
        ],
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            Popper: ['popper.js', 'default'],
        }),
    ],
};