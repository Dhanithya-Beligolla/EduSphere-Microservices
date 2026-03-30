const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');

const User = sequelize.define(
  'User',
  {
    id: {
        type: DataTypes.UUID,
        defaultValue: DataTypes.UUIDV4,
        primaryKey: true
    },
    firstName: {
        type: DataTypes.STRING(100),
        allowNull: false,
        field: 'first_name'
    },
    lastName: {
        type: DataTypes.STRING(100),
        allowNull: false,
        field: 'last_name'
    },
    email: {
        type: DataTypes.STRING(150),
        allowNull: false,
        unique: true,
        validate: {
            isEmail: true
        }
    },
    username: {
        type: DataTypes.STRING(100),
        allowNull: false,
        unique: true
    },
    roleId: {
        type: DataTypes.INTEGER,
        allowNull: false,
        field: 'role_id',
        references: {
            model: 'roles',
            key: 'id'
        }
    },
    passwordHash: {
        type: DataTypes.STRING(255),
        allowNull: false,
        field: 'password_hash'
    },
    phone: {
        type: DataTypes.STRING(20),
        allowNull: true
    },
    isActive: {
        type: DataTypes.BOOLEAN,
        allowNull: false,
        defaultValue: true,
        field: 'is_active'
    },
    isEmailVerified: {
        type: DataTypes.BOOLEAN,
        allowNull: false,
        defaultValue: false,
        field: 'is_email_verified'
    },
    createdBy: {
        type: DataTypes.UUID,
        allowNull: true,
        field: 'created_by'
    },
    updatedBy: {
        type: DataTypes.UUID,
        allowNull: true,
        field: 'updated_by'
        }
  },
  {
    tableName: 'users',
    underscored: true,
    timestamps: true,
    defaultScope: {
        attributes: { exclude: ['passwordHash'] }
    },
    scopes: {
        withPassword: {
            attributes: { include: ['passwordHash'] }
        }
    }
  }
);

module.exports = User;