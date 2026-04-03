const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const swaggerUi = require('swagger-ui-express');
const connectDB = require('./config/db');
const routes = require('./routes');
const { registerEventListeners } = require('./events/academicEvents');

const app = express();

const ACADEMIC_OPENAPI_PATHS = {
  '/api/health': {
    get: {
      tags: ['System'],
      summary: 'Health check',
      responses: {
        200: { description: 'Service health status' },
      },
    },
  },
  '/api/academic-years': {
    get: {
      tags: ['Academic Years'],
      summary: 'List academic years',
      responses: { 200: { description: 'Academic years list' } },
    },
    post: {
      tags: ['Academic Years'],
      summary: 'Create academic year',
      responses: { 201: { description: 'Academic year created' } },
    },
  },
  '/api/academic-years/active': {
    get: {
      tags: ['Academic Years'],
      summary: 'Get active academic year',
      responses: { 200: { description: 'Active academic year' } },
    },
  },
  '/api/academic-years/{id}/activate': {
    patch: {
      tags: ['Academic Years'],
      summary: 'Activate academic year',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Academic year activated' } },
    },
  },
  '/api/academic-years/{id}': {
    delete: {
      tags: ['Academic Years'],
      summary: 'Delete academic year',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Academic year deleted' } },
    },
  },
  '/api/grades': {
    get: {
      tags: ['Grades'],
      summary: 'List grades',
      responses: { 200: { description: 'Grades list' } },
    },
    post: {
      tags: ['Grades'],
      summary: 'Create grade',
      responses: { 201: { description: 'Grade created' } },
    },
  },
  '/api/grades/{id}': {
    put: {
      tags: ['Grades'],
      summary: 'Update grade',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Grade updated' } },
    },
    delete: {
      tags: ['Grades'],
      summary: 'Delete grade',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Grade deleted' } },
    },
  },
  '/api/sections': {
    get: {
      tags: ['Sections'],
      summary: 'List sections',
      responses: { 200: { description: 'Sections list' } },
    },
    post: {
      tags: ['Sections'],
      summary: 'Create section',
      responses: { 201: { description: 'Section created' } },
    },
  },
  '/api/sections/{id}': {
    put: {
      tags: ['Sections'],
      summary: 'Update section',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Section updated' } },
    },
    delete: {
      tags: ['Sections'],
      summary: 'Delete section',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Section deleted' } },
    },
  },
  '/api/subjects': {
    get: {
      tags: ['Subjects'],
      summary: 'List subjects',
      responses: { 200: { description: 'Subjects list' } },
    },
    post: {
      tags: ['Subjects'],
      summary: 'Create subject',
      responses: { 201: { description: 'Subject created' } },
    },
  },
  '/api/subjects/{id}': {
    get: {
      tags: ['Subjects'],
      summary: 'Get subject by id',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Subject details' } },
    },
    put: {
      tags: ['Subjects'],
      summary: 'Update subject',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Subject updated' } },
    },
    delete: {
      tags: ['Subjects'],
      summary: 'Delete subject',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Subject deleted' } },
    },
  },
  '/api/enrollments': {
    get: {
      tags: ['Enrollments'],
      summary: 'List enrollments',
      responses: { 200: { description: 'Enrollments list' } },
    },
    post: {
      tags: ['Enrollments'],
      summary: 'Enroll student',
      responses: { 201: { description: 'Student enrolled' } },
    },
  },
  '/api/enrollments/student/{studentId}': {
    get: {
      tags: ['Enrollments'],
      summary: 'Get student enrollment',
      parameters: [{ name: 'studentId', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Student enrollment details' } },
    },
  },
  '/api/enrollments/{id}/transfer': {
    patch: {
      tags: ['Enrollments'],
      summary: 'Transfer student enrollment',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Enrollment transferred' } },
    },
  },
  '/api/enrollments/promote': {
    post: {
      tags: ['Enrollments'],
      summary: 'Promote students',
      responses: { 200: { description: 'Students promoted' } },
    },
  },
  '/api/teacher-assignments': {
    get: {
      tags: ['Teacher Assignments'],
      summary: 'List teacher assignments',
      responses: { 200: { description: 'Teacher assignments list' } },
    },
    post: {
      tags: ['Teacher Assignments'],
      summary: 'Create teacher assignment',
      responses: { 201: { description: 'Teacher assignment created' } },
    },
  },
  '/api/teacher-assignments/teaching-load/{teacherId}': {
    get: {
      tags: ['Teacher Assignments'],
      summary: 'Get teaching load',
      parameters: [{ name: 'teacherId', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Teaching load details' } },
    },
  },
  '/api/teacher-assignments/{id}': {
    delete: {
      tags: ['Teacher Assignments'],
      summary: 'Delete teacher assignment',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Teacher assignment deleted' } },
    },
  },
  '/api/timetable': {
    get: {
      tags: ['Timetable'],
      summary: 'Get timetable',
      responses: { 200: { description: 'Timetable slots list' } },
    },
    post: {
      tags: ['Timetable'],
      summary: 'Create timetable slot',
      responses: { 201: { description: 'Timetable slot created' } },
    },
  },
  '/api/timetable/bulk': {
    post: {
      tags: ['Timetable'],
      summary: 'Create timetable slots in bulk',
      responses: { 201: { description: 'Bulk slots created' } },
    },
  },
  '/api/timetable/{id}': {
    put: {
      tags: ['Timetable'],
      summary: 'Update timetable slot',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Timetable slot updated' } },
    },
    delete: {
      tags: ['Timetable'],
      summary: 'Delete timetable slot',
      parameters: [{ name: 'id', in: 'path', required: true, schema: { type: 'string' } }],
      responses: { 200: { description: 'Timetable slot deleted' } },
    },
  },
  '/api/timetable/publish': {
    post: {
      tags: ['Timetable'],
      summary: 'Publish timetable',
      responses: { 200: { description: 'Timetable published' } },
    },
  },
};

const swaggerDocs = {
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
  paths: ACADEMIC_OPENAPI_PATHS,
};

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
app.get('/api-docs.json', (req, res) => {
  res.json(swaggerDocs);
});

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