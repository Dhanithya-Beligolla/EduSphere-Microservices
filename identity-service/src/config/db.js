const { Sequelize } = require('sequelize');
const env = require('./env');

const commonOptions = {
  dialect: 'postgres',
  logging: false
};

let sequelize;

if (env.databaseUrl) {
  sequelize = new Sequelize(env.databaseUrl, {
    ...commonOptions,
    dialectOptions: env.dbSsl
      ? {
          ssl: {
            require: true,
            rejectUnauthorized: false
          }
        }
      : {}
  });
} else {
  sequelize = new Sequelize(env.dbName, env.dbUser, env.dbPassword, {
    ...commonOptions,
    host: env.dbHost,
    port: env.dbPort
  });
}

module.exports = sequelize;