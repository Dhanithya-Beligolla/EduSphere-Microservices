// src/routes/index.js

const express = require('express');
const authRoutes = require('./auth.routes');
const env = require('../config/env');

const router = express.Router();

router.use(`${env.apiPrefix}/auth`, authRoutes);

module.exports = router;
