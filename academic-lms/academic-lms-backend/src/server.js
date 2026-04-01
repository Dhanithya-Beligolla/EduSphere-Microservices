const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');
const connectDB = require('./config/db');
const routes = require('./routes');
const { registerEventListeners } = require('./events/academicEvents');

const app = express();

const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Academic Management Service API',
      version: '1.0.0',
      description: 'LMS Academic Management Service Documentation',
    },
    servers: [
      {
        url: `http://localhost:${process.env.PORT || 4003}`,
      },
    ],
  },
  apis: [path.join(__dirname, './routes/*.js'), path.join(__dirname, 'server.js')],
};

const swaggerDocs = swaggerJsdoc(swaggerOptions);

app.use(
  cors({
    origin: process.env.CLIENT_URL || 'http://localhost:3000',
    credentials: true,
  })
);

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

if (process.env.NODE_ENV === 'development') {
  app.use(morgan('dev'));
}

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'Academic Management Service',
    timestamp: new Date(),
  });
});

app.use('/api', routes);

app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: `Route ${req.originalUrl} not found`,
  });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.statusCode || 500).json({
    success: false,
    message: err.message || 'Internal Server Error',
  });
});

const PORT = process.env.PORT || 4003;

const start = async () => {
  try {
    await connectDB();
    registerEventListeners();
    app.listen(PORT, () => {
      console.log(`🚀 Academic Management Service running on port ${PORT}`);
      console.log(`📖 Swagger Docs: http://localhost:${PORT}/api-docs`);
    });
  } catch (error) {
    console.error('❌ Server startup error:', error.message);
    process.exit(1);
  }
};

start();