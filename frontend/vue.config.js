module.exports = {
    publicPath: '/',
    devServer: {
        port: 80,
        public:  process.env.NODE_ENV === 'production' ? process.env.DOMAIN_NAME : process.env.DEV_DOMAIN_NAME,
    },
    outputDir: 'dist/dist',
    configureWebpack: {
        resolve: { symlinks: false },
        devtool: 'source-map',
        devServer: {
            watchOptions: {
                poll: true
            }
        },
    }
};
