module.exports = {
    PORT: process.env.PORT || 3000,
    DB_URI: process.env.DB_URI || 'mongodb://localhost:27017/mydatabase',
    NODE_ENV: process.env.NODE_ENV || 'development',
    API_KEY: process.env.API_KEY || '',
};