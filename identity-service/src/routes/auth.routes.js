// src/routes/auth.routes.js

const express = require('express');
const authController = require('../controllers/auth.controller');
const authMiddleware = require('../middlewares/auth.middleware');
const roleMiddleware = require('../middlewares/role.middleware');
const validate = require('../middlewares/validate.middleware');
const {
  registerValidator,
  loginValidator,
  updateStatusValidator
} = require('../validators/auth.validator');
const asyncHandler = require('../utils/asyncHandler');

const router = express.Router();

router.post('/login', loginValidator, validate, asyncHandler(authController.login));

router.post(
  '/register',
  authMiddleware,
  roleMiddleware('SUPER_ADMIN', 'ADMIN'),
  registerValidator,
  validate,
  asyncHandler(authController.register)
);

router.get('/me', authMiddleware, asyncHandler(authController.me));
router.get('/verify', authMiddleware, asyncHandler(authController.verify));

router.get(
  '/users',
  authMiddleware,
  roleMiddleware('SUPER_ADMIN', 'ADMIN'),
  asyncHandler(authController.listUsers)
);

router.get(
  '/users/:id',
  authMiddleware,
  roleMiddleware('SUPER_ADMIN', 'ADMIN'),
  asyncHandler(authController.getUserById)
);

router.patch(
  '/users/:id/status',
  authMiddleware,
  roleMiddleware('SUPER_ADMIN', 'ADMIN'),
  updateStatusValidator,
  validate,
  asyncHandler(authController.updateUserStatus)
);

module.exports = router;
