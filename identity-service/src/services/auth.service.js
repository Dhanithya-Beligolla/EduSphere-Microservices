// src/services/auth.service.js

const bcrypt = require('bcrypt');
const { Op } = require('sequelize');
const { User, Role } = require('../models');
const { signAccessToken } = require('../config/jwt');
const ApiError = require('../utils/ApiError');

const SALT_ROUNDS = 10;

function sanitizeUser(userInstance) {
  const user = userInstance.toJSON();
  delete user.passwordHash;

  return {
    id: user.id,
    firstName: user.firstName,
    lastName: user.lastName,
    email: user.email,
    username: user.username,
    phone: user.phone,
    isActive: user.isActive,
    isEmailVerified: user.isEmailVerified,
    role: user.role?.name || null,
    createdAt: user.createdAt,
    updatedAt: user.updatedAt
  };
}

function canCreateRole(requesterRole, targetRole) {
  const matrix = {
    SUPER_ADMIN: [
      'SUPER_ADMIN',
      'ADMIN',
      'PRINCIPAL',
      'DEPUTY_PRINCIPAL',
      'SECTIONAL_HEAD',
      'CLASS_TEACHER',
      'SUBJECT_TEACHER',
      'STUDENT',
      'PARENT'
    ],
    ADMIN: [
      'PRINCIPAL',
      'DEPUTY_PRINCIPAL',
      'SECTIONAL_HEAD',
      'CLASS_TEACHER',
      'SUBJECT_TEACHER',
      'STUDENT',
      'PARENT'
    ]
  };

  return (matrix[requesterRole] || []).includes(targetRole);
}

async function registerUser(payload, creator) {
  if (!creator?.role) {
    throw new ApiError(401, 'Unauthorized');
  }

  if (!canCreateRole(creator.role, payload.role)) {
    throw new ApiError(403, `Role ${creator.role} cannot create ${payload.role}`);
  }

  const existingUser = await User.scope('withPassword').findOne({
    where: {
      [Op.or]: [{ email: payload.email }, { username: payload.username }]
    }
  });

  if (existingUser) {
    throw new ApiError(409, 'Email or username already exists');
  }

  const role = await Role.findOne({ where: { name: payload.role } });
  if (!role) {
    throw new ApiError(404, 'Role not found');
  }

  const passwordHash = await bcrypt.hash(payload.password, SALT_ROUNDS);

  const createdUser = await User.create({
    firstName: payload.firstName,
    lastName: payload.lastName,
    email: payload.email,
    username: payload.username,
    passwordHash,
    phone: payload.phone || null,
    roleId: role.id,
    createdBy: creator.sub,
    updatedBy: creator.sub
  });

  const userWithRole = await User.findByPk(createdUser.id, {
    include: [{ model: Role, as: 'role', attributes: ['id', 'name', 'description'] }]
  });

  return sanitizeUser(userWithRole);
}

async function loginUser({ emailOrUsername, password }) {
  const user = await User.scope('withPassword').findOne({
    where: {
      [Op.or]: [{ email: emailOrUsername }, { username: emailOrUsername }]
    },
    include: [{ model: Role, as: 'role', attributes: ['id', 'name', 'description'] }]
  });

  if (!user) {
    throw new ApiError(401, 'Invalid credentials');
  }

  if (!user.isActive) {
    throw new ApiError(403, 'User account is inactive');
  }

  const isPasswordValid = await bcrypt.compare(password, user.passwordHash);
  if (!isPasswordValid) {
    throw new ApiError(401, 'Invalid credentials');
  }

  const token = signAccessToken({
    id: user.id,
    email: user.email,
    username: user.username,
    roleName: user.role.name
  });

  return {
    accessToken: token,
    user: sanitizeUser(user)
  };
}

async function getCurrentUser(userId) {
  const user = await User.findByPk(userId, {
    include: [{ model: Role, as: 'role', attributes: ['id', 'name', 'description'] }]
  });

  if (!user) {
    throw new ApiError(404, 'User not found');
  }

  return sanitizeUser(user);
}

async function verifyUser(userId) {
  const user = await User.findByPk(userId, {
    include: [{ model: Role, as: 'role', attributes: ['id', 'name', 'description'] }]
  });

  if (!user) {
    throw new ApiError(404, 'User not found');
  }

  return {
    valid: true,
    user: {
      id: user.id,
      email: user.email,
      username: user.username,
      role: user.role?.name || null,
      isActive: user.isActive
    }
  };
}

async function listUsers() {
  const users = await User.findAll({
    order: [['createdAt', 'DESC']],
    include: [{ model: Role, as: 'role', attributes: ['id', 'name', 'description'] }]
  });

  return users.map(sanitizeUser);
}

async function getUserById(id) {
  const user = await User.findByPk(id, {
    include: [{ model: Role, as: 'role', attributes: ['id', 'name', 'description'] }]
  });

  if (!user) {
    throw new ApiError(404, 'User not found');
  }

  return sanitizeUser(user);
}

async function updateUserStatus(id, isActive, actor) {
  const user = await User.findByPk(id, {
    include: [{ model: Role, as: 'role', attributes: ['id', 'name', 'description'] }]
  });

  if (!user) {
    throw new ApiError(404, 'User not found');
  }

  user.isActive = isActive;
  user.updatedBy = actor.sub;
  await user.save();

  const updated = await User.findByPk(id, {
    include: [{ model: Role, as: 'role', attributes: ['id', 'name', 'description'] }]
  });

  return sanitizeUser(updated);
}

module.exports = {
  registerUser,
  loginUser,
  getCurrentUser,
  verifyUser,
  listUsers,
  getUserById,
  updateUserStatus
};
