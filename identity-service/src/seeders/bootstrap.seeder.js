// src/seeders/bootstrap.seeder.js


const bcrypt = require('bcrypt');
const env = require('../config/env');
const { Role, User } = require('../models');

const roles = [
  { name: 'SUPER_ADMIN', description: 'System super administrator' },
  { name: 'ADMIN', description: 'System administrator' },
  { name: 'PRINCIPAL', description: 'School principal' },
  { name: 'DEPUTY_PRINCIPAL', description: 'Deputy or assistant principal' },
  { name: 'SECTIONAL_HEAD', description: 'Sectional or stream head' },
  { name: 'CLASS_TEACHER', description: 'Class teacher' },
  { name: 'SUBJECT_TEACHER', description: 'Subject teacher' },
  { name: 'STUDENT', description: 'Student' },
  { name: 'PARENT', description: 'Parent or guardian' }
];

async function seedRoles() {
  for (const role of roles) {
    await Role.findOrCreate({
      where: { name: role.name },
      defaults: role
    });
  }
}

async function seedSuperAdmin() {
  const role = await Role.findOne({ where: { name: 'SUPER_ADMIN' } });
  if (!role) return;

  const existing = await User.scope('withPassword').findOne({
    where: { email: env.superAdmin.email }
  });

  if (existing) return;

  const passwordHash = await bcrypt.hash(env.superAdmin.password, 10);

  await User.create({
    firstName: env.superAdmin.firstName,
    lastName: env.superAdmin.lastName,
    email: env.superAdmin.email,
    username: env.superAdmin.username,
    passwordHash,
    roleId: role.id,
    isActive: true,
    isEmailVerified: true
  });
}

async function bootstrapSeed() {
  await seedRoles();
  await seedSuperAdmin();
}

module.exports = bootstrapSeed;
