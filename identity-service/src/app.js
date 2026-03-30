// src/app.js

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const routes = require('./routes');
const errorMiddleware = require('./middlewares/error.middleware');
const { sendSuccess } = require('./utils/response');

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev'));

app.get('/health', (req, res) => {
  return sendSuccess(res, 200, 'Identity service is healthy', {
    service: 'identity-service'
  });
});

app.use(routes);

app.use((req, res) => {
  return res.status(404).json({
    success: false,
    message: 'Route not found',
    data: null,
    errors: []
  });
});

app.use(errorMiddleware);

module.exports = app;
