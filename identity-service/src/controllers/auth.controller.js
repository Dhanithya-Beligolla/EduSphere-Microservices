// src/controllers/auth.controller.js

const authService = require('../services/auth.service');
const { sendSuccess } = require('../utils/response');

exports.register = async (req, res) => {
  const user = await authService.registerUser(req.body, req.user);
  return sendSuccess(res, 201, 'User registered successfully', user);
};

exports.login = async (req, res) => {
  const result = await authService.loginUser(req.body);
  return sendSuccess(res, 200, 'Login successful', result);
};

exports.me = async (req, res) => {
  const user = await authService.getCurrentUser(req.user.sub);
  return sendSuccess(res, 200, 'Current user fetched successfully', user);
};

exports.verify = async (req, res) => {
  const result = await authService.verifyUser(req.user.sub);
  return sendSuccess(res, 200, 'Token is valid', result);
};

exports.listUsers = async (req, res) => {
  const users = await authService.listUsers();
  return sendSuccess(res, 200, 'Users fetched successfully', users);
};

exports.getUserById = async (req, res) => {
  const user = await authService.getUserById(req.params.id);
  return sendSuccess(res, 200, 'User fetched successfully', user);
};

exports.updateUserStatus = async (req, res) => {
  const updatedUser = await authService.updateUserStatus(
    req.params.id,
    req.body.isActive,
    req.user
  );

  return sendSuccess(res, 200, 'User status updated successfully', updatedUser);
};
