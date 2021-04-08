module.exports = {
    publicPath: '/',
    devServer: {
        port: 80,
        public:  process.env.NODE_ENV === 'production' ? process.env.DOMAIN_NAME : process.env.DEV_DOMAIN_NAME,
    },
    configureWebpack: {
        resolve: { symlinks: false },
        devtool: 'source-map',
        //watch: true,
        //watchOptions: {
        //    aggregateTimeout: 1000,
        //    poll: 5000,
        //    ignored: /node_modules/
        //},
        devServer: {
            watchOptions: {
                poll: true
            }
        },
        //optimization: {
        //    splitChunks: {
        //        minSize: 10000,
        //        maxSize: 250000,
        //    }
        //}
    }
};
