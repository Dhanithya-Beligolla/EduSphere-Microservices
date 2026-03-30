// src/server.js
const app = require('./app');
const env = require('./config/env');
const sequelize = require('./config/db');
require('./models');
const bootstrapSeed = require('./seeders/bootstrap.seeder');

async function startServer() {
  try {
    await sequelize.authenticate();
    console.log('Database connection established successfully.');

    await sequelize.sync({ alter: true });
    console.log('Database synced successfully.');

    await bootstrapSeed();
    console.log('Bootstrap seed completed successfully.');

    app.listen(env.port, () => {
      console.log(`${env.appName} running on port ${env.port}`);
    });
  } catch (error) {
    console.error('Failed to start service:', error);
    process.exit(1);
  }
}

startServer();

