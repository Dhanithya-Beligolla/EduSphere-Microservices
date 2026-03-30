const swaggerJSDoc = require('swagger-jsdoc');
const env = require('../config/env');

const roleEnum = [
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

const options = {
  definition: {
    openapi: '3.0.3',
    info: {
      title: 'Identity Service API',
      version: '1.0.0',
      description:
        'Authentication and user identity management API for EduSphere microservices.'
    },
    servers: [
      {
        url: `http://localhost:${env.port}`,
        description: 'Local'
      }
    ],
    tags: [
      {
        name: 'Auth',
        description: 'Authentication and user management endpoints'
      }
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT'
        }
      },
      schemas: {
        ApiErrorItem: {
          type: 'object',
          properties: {
            field: { type: 'string', example: 'email' },
            message: { type: 'string', example: 'A valid email is required' }
          },
          additionalProperties: true
        },
        ApiErrorResponse: {
          type: 'object',
          properties: {
            success: { type: 'boolean', example: false },
            message: { type: 'string', example: 'Unauthorized' },
            data: { nullable: true, example: null },
            errors: {
              type: 'array',
              items: { $ref: '#/components/schemas/ApiErrorItem' }
            }
          }
        },
        Role: {
          type: 'string',
          enum: roleEnum,
          example: 'ADMIN'
        },
        User: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            firstName: { type: 'string', example: 'John' },
            lastName: { type: 'string', example: 'Doe' },
            email: { type: 'string', format: 'email', example: 'john@school.com' },
            username: { type: 'string', example: 'john.doe' },
            phone: { type: 'string', nullable: true, example: '+94771234567' },
            isActive: { type: 'boolean', example: true },
            isEmailVerified: { type: 'boolean', example: false },
            role: { $ref: '#/components/schemas/Role' },
            createdAt: { type: 'string', format: 'date-time' },
            updatedAt: { type: 'string', format: 'date-time' }
          }
        },
        LoginRequest: {
          type: 'object',
          required: ['emailOrUsername', 'password'],
          properties: {
            emailOrUsername: {
              type: 'string',
              example: 'superadmin@lms.com'
            },
            password: {
              type: 'string',
              example: 'Super@12345'
            }
          }
        },
        RegisterRequest: {
          type: 'object',
          required: ['firstName', 'lastName', 'email', 'username', 'password', 'role'],
          properties: {
            firstName: { type: 'string', example: 'Jane' },
            lastName: { type: 'string', example: 'Smith' },
            email: { type: 'string', format: 'email', example: 'jane@school.com' },
            username: { type: 'string', example: 'jane.smith' },
            password: { type: 'string', minLength: 8, example: 'Pass@1234' },
            role: { $ref: '#/components/schemas/Role' },
            phone: { type: 'string', example: '+94771234567' }
          }
        },
        UpdateStatusRequest: {
          type: 'object',
          required: ['isActive'],
          properties: {
            isActive: {
              type: 'boolean',
              example: false
            }
          }
        },
        LoginData: {
          type: 'object',
          properties: {
            accessToken: { type: 'string' },
            user: { $ref: '#/components/schemas/User' }
          }
        },
        VerifyData: {
          type: 'object',
          properties: {
            valid: { type: 'boolean', example: true },
            user: {
              type: 'object',
              properties: {
                id: { type: 'string', format: 'uuid' },
                email: { type: 'string', format: 'email' },
                username: { type: 'string' },
                role: { $ref: '#/components/schemas/Role' },
                isActive: { type: 'boolean' }
              }
            }
          }
        },
        SuccessLoginResponse: {
          type: 'object',
          properties: {
            success: { type: 'boolean', example: true },
            message: { type: 'string', example: 'Login successful' },
            data: { $ref: '#/components/schemas/LoginData' },
            errors: { type: 'array', items: {} }
          }
        },
        SuccessUserResponse: {
          type: 'object',
          properties: {
            success: { type: 'boolean', example: true },
            message: { type: 'string', example: 'User fetched successfully' },
            data: { $ref: '#/components/schemas/User' },
            errors: { type: 'array', items: {} }
          }
        },
        SuccessUsersResponse: {
          type: 'object',
          properties: {
            success: { type: 'boolean', example: true },
            message: { type: 'string', example: 'Users fetched successfully' },
            data: {
              type: 'array',
              items: { $ref: '#/components/schemas/User' }
            },
            errors: { type: 'array', items: {} }
          }
        },
        SuccessVerifyResponse: {
          type: 'object',
          properties: {
            success: { type: 'boolean', example: true },
            message: { type: 'string', example: 'Token is valid' },
            data: { $ref: '#/components/schemas/VerifyData' },
            errors: { type: 'array', items: {} }
          }
        }
      }
    },
    paths: {
      [`${env.apiPrefix}/auth/login`]: {
        post: {
          tags: ['Auth'],
          summary: 'Authenticate user',
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/LoginRequest' }
              }
            }
          },
          responses: {
            200: {
              description: 'Login successful',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/SuccessLoginResponse' }
                }
              }
            },
            401: {
              description: 'Invalid credentials',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            403: {
              description: 'Inactive account',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            422: {
              description: 'Validation failed',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            }
          }
        }
      },
      [`${env.apiPrefix}/auth/register`]: {
        post: {
          tags: ['Auth'],
          summary: 'Create a user account by role-restricted admin',
          security: [{ bearerAuth: [] }],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/RegisterRequest' }
              }
            }
          },
          responses: {
            201: {
              description: 'User registered successfully',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/SuccessUserResponse' }
                }
              }
            },
            401: {
              description: 'Unauthorized',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            403: {
              description: 'Role is not allowed to create target user',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            409: {
              description: 'Email or username already exists',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            422: {
              description: 'Validation failed',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            }
          }
        }
      },
      [`${env.apiPrefix}/auth/me`]: {
        get: {
          tags: ['Auth'],
          summary: 'Get current authenticated user',
          security: [{ bearerAuth: [] }],
          responses: {
            200: {
              description: 'Current user fetched successfully',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/SuccessUserResponse' }
                }
              }
            },
            401: {
              description: 'Unauthorized',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            404: {
              description: 'User not found',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            }
          }
        }
      },
      [`${env.apiPrefix}/auth/verify`]: {
        get: {
          tags: ['Auth'],
          summary: 'Verify access token and resolve user claims',
          security: [{ bearerAuth: [] }],
          responses: {
            200: {
              description: 'Token is valid',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/SuccessVerifyResponse' }
                }
              }
            },
            401: {
              description: 'Invalid or expired token',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            404: {
              description: 'User not found',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            }
          }
        }
      },
      [`${env.apiPrefix}/auth/users`]: {
        get: {
          tags: ['Auth'],
          summary: 'List all users (SUPER_ADMIN, ADMIN)',
          security: [{ bearerAuth: [] }],
          responses: {
            200: {
              description: 'Users fetched successfully',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/SuccessUsersResponse' }
                }
              }
            },
            401: {
              description: 'Unauthorized',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            403: {
              description: 'Forbidden',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            }
          }
        }
      },
      [`${env.apiPrefix}/auth/users/{id}`]: {
        get: {
          tags: ['Auth'],
          summary: 'Get user by ID (SUPER_ADMIN, ADMIN)',
          security: [{ bearerAuth: [] }],
          parameters: [
            {
              in: 'path',
              name: 'id',
              required: true,
              schema: { type: 'string', format: 'uuid' }
            }
          ],
          responses: {
            200: {
              description: 'User fetched successfully',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/SuccessUserResponse' }
                }
              }
            },
            401: {
              description: 'Unauthorized',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            403: {
              description: 'Forbidden',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            404: {
              description: 'User not found',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            }
          }
        }
      },
      [`${env.apiPrefix}/auth/users/{id}/status`]: {
        patch: {
          tags: ['Auth'],
          summary: 'Update user active status (SUPER_ADMIN, ADMIN)',
          security: [{ bearerAuth: [] }],
          parameters: [
            {
              in: 'path',
              name: 'id',
              required: true,
              schema: { type: 'string', format: 'uuid' }
            }
          ],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/UpdateStatusRequest' }
              }
            }
          },
          responses: {
            200: {
              description: 'User status updated successfully',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/SuccessUserResponse' }
                }
              }
            },
            401: {
              description: 'Unauthorized',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            403: {
              description: 'Forbidden',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            404: {
              description: 'User not found',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            },
            422: {
              description: 'Validation failed',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ApiErrorResponse' }
                }
              }
            }
          }
        }
      }
    }
  },
  apis: []
};

const swaggerSpec = swaggerJSDoc(options);

module.exports = swaggerSpec;
