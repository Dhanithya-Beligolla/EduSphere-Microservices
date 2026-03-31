const { body, param } = require('express-validator');

const allowedRoles = [
  'SUPER_ADMIN',
  'ADMIN',
  'PRINCIPAL',
  'DEPUTY_PRINCIPAL',
  'SECTIONAL_HEAD',
  'CLASS_TEACHER',
  'SUBJECT_TEACHER',
  'STUDENT',
  'PARENT'
];

const registerValidator = [
  body('firstName').trim().notEmpty().withMessage('First name is required'),
  body('lastName').trim().notEmpty().withMessage('Last name is required'),
  body('email').trim().isEmail().withMessage('A valid email is required'),
  body('username').trim().notEmpty().withMessage('Username is required'),
  body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters long'),
  body('role')
    .trim()
    .isIn(allowedRoles)
    .withMessage('Invalid role'),
  body('phone').optional().trim().isLength({ min: 7 }).withMessage('Invalid phone number')
];

const loginValidator = [
  body('emailOrUsername')
    .trim()
    .notEmpty()
    .withMessage('Email or username is required'),
  body('password').notEmpty().withMessage('Password is required')
];

const updateStatusValidator = [
  param('id').isUUID().withMessage('Invalid user id'),
  body('isActive').isBoolean().withMessage('isActive must be boolean')
];

module.exports = {
  registerValidator,
  loginValidator,
  updateStatusValidator,
  allowedRoles
};