module.exports = {
    env: process.env.NODE_ENV,
    development: {
        port: process.env.PORT,
        db: {
            uri: process.env.MONGODB_URI
        },
        logging: {
            enabled: true,
            format: 'dev'
        },
        cors: {
            origin: process.env.CORS_ORIGIN
        },
        https: false
    },
    production: {
        port: process.env.PORT,
        db: {
            uri: process.env.MONGODB_URI
        },
        logging: {
            enabled: false
        },
        cors: {
            origin: process.env.CORS_ORIGIN
        },
        https: false
    }
};
