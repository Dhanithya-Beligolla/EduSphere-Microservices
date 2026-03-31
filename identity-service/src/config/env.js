// src/config/env.js

const dotenv = require('dotenv');

dotenv.config();

module.exports = {
  port: process.env.PORT || 4001,
  nodeEnv: process.env.NODE_ENV || 'development',
  appName: process.env.APP_NAME || 'identity-service',
  apiPrefix: process.env.API_PREFIX || '/api/v1',

  jwtSecret: process.env.JWT_SECRET || 'change_me',
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '1d',

  databaseUrl: process.env.DATABASE_URL || '',
  dbHost: process.env.DB_HOST || 'localhost',
  dbPort: Number(process.env.DB_PORT || 5432),
  dbName: process.env.DB_NAME || 'identity_db',
  dbUser: process.env.DB_USER || 'postgres',
  dbPassword: process.env.DB_PASSWORD || 'postgres',
  dbSsl: String(process.env.DB_SSL || 'false') === 'true',

  superAdmin: {
    firstName: process.env.SUPERADMIN_FIRST_NAME || 'Super',
    lastName: process.env.SUPERADMIN_LAST_NAME || 'Admin',
    email: process.env.SUPERADMIN_EMAIL || 'superadmin@lms.com',
    username: process.env.SUPERADMIN_USERNAME || 'superadmin',
    password: process.env.SUPERADMIN_PASSWORD || 'Super@12345'
  }
};