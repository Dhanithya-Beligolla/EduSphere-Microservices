const sequelize = require('../config/db');
const Role = require('./role.model');
const User = require('./user.model');

Role.hasMany(User, {
  foreignKey: 'role_id',
  as: 'users'
});

User.belongsTo(Role, {
  foreignKey: 'role_id',
  as: 'role'
});

module.exports = {
  sequelize,
  Role,
  User
};