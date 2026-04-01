require('dotenv').config();
const mongoose = require('mongoose');
const connectDB = require('./db');
const User = require('../models/User');
const AcademicYear = require('../models/AcademicYear');
const { Grade } = require('../models/Grade');
const Stream = require('../models/Stream');
const Subject = require('../models/Subject');

const seed = async () => {
  await connectDB();
  console.log('🌱 Seeding database...');

  // Clear existing
  await Promise.all([
    User.deleteMany({}),
    AcademicYear.deleteMany({}),
    Grade.deleteMany({}),
    Stream.deleteMany({}),
    Subject.deleteMany({}),
  ]);

  // Academic Year
  const year = await AcademicYear.create({
    year: '2024',
    startDate: new Date('2024-01-08'),
    endDate: new Date('2024-12-13'),
    isActive: true,
    terms: [
      { name: 'Term 1', startDate: new Date('2024-01-08'), endDate: new Date('2024-04-12'), isActive: false },
      { name: 'Term 2', startDate: new Date('2024-05-06'), endDate: new Date('2024-08-09'), isActive: true },
      { name: 'Term 3', startDate: new Date('2024-09-02'), endDate: new Date('2024-12-13'), isActive: false },
    ],
  });

  // Streams (A/L)
  const streams = await Stream.insertMany([
    { name: 'Science', code: 'SCI', applicableGrades: [12, 13] },
    { name: 'Arts', code: 'ART', applicableGrades: [12, 13] },
    { name: 'Commerce', code: 'COM', applicableGrades: [12, 13] },
    { name: 'Technology', code: 'TECH', applicableGrades: [12, 13] },
  ]);

  // Subjects
  await Subject.insertMany([
    { name: 'Mathematics', code: 'MATH', applicableGrades: [6,7,8,9,10,11], periodsPerWeek: 6 },
    { name: 'Science', code: 'SCI', applicableGrades: [6,7,8,9,10,11], periodsPerWeek: 5 },
    { name: 'English', code: 'ENG', applicableGrades: [6,7,8,9,10,11,12,13], periodsPerWeek: 5 },
    { name: 'Sinhala', code: 'SIN', applicableGrades: [6,7,8,9,10,11], periodsPerWeek: 5 },
    { name: 'History', code: 'HIST', applicableGrades: [6,7,8,9,10,11], periodsPerWeek: 3 },
    { name: 'Geography', code: 'GEO', applicableGrades: [6,7,8,9,10,11], periodsPerWeek: 3 },
    { name: 'Tamil', code: 'TAM', applicableGrades: [6,7,8,9,10], periodsPerWeek: 4 },
    { name: 'Buddhism', code: 'BUD', applicableGrades: [6,7,8,9,10,11], periodsPerWeek: 2 },
    { name: 'ICT', code: 'ICT', applicableGrades: [6,7,8,9,10,11,12,13], periodsPerWeek: 3 },
    { name: 'Combined Mathematics', code: 'CMATH', applicableGrades: [12,13], periodsPerWeek: 8, type: 'optional' },
  ]);

  // Grades
  await Grade.insertMany([
    { name: 'Grade 6', level: 6, division: 'junior_secondary', academicYear: year._id },
    { name: 'Grade 7', level: 7, division: 'junior_secondary', academicYear: year._id },
    { name: 'Grade 8', level: 8, division: 'junior_secondary', academicYear: year._id },
    { name: 'Grade 9', level: 9, division: 'junior_secondary', academicYear: year._id },
    { name: 'Grade 10', level: 10, division: 'senior_secondary', academicYear: year._id },
    { name: 'Grade 11', level: 11, division: 'senior_secondary', academicYear: year._id },
    { name: 'Grade 12', level: 12, division: 'al', academicYear: year._id },
    { name: 'Grade 13', level: 13, division: 'al', academicYear: year._id },
  ]);

  // Users
  await User.insertMany([
    {
      firstName: 'Nimali', lastName: 'Perera',
      email: 'admin@school.lk', password: 'password123',
      role: 'admin', employeeId: 'ADM001',
    },
    {
      firstName: 'Rohan', lastName: 'Silva',
      email: 'principal@school.lk', password: 'password123',
      role: 'principal', employeeId: 'PRI001',
    },
    {
      firstName: 'Kamala', lastName: 'Fernando',
      email: 'teacher1@school.lk', password: 'password123',
      role: 'subject_teacher', employeeId: 'TCH001',
      qualifications: ['BSc Mathematics', 'PGDE'],
    },
    {
      firstName: 'Sunil', lastName: 'Bandara',
      email: 'teacher2@school.lk', password: 'password123',
      role: 'class_teacher', employeeId: 'TCH002',
    },
    {
      firstName: 'Kavya', lastName: 'Jayawardena',
      email: 'student1@school.lk', password: 'password123',
      role: 'student', parentName: 'Priya Jayawardena', parentPhone: '0771234567',
    },
  ]);

  console.log('✅ Seed complete!');
  console.log('👤 Admin: admin@school.lk / password123');
  console.log('👤 Principal: principal@school.lk / password123');
  await mongoose.connection.close();
};

seed().catch((err) => {
  console.error('❌ Seed failed:', err);
  process.exit(1);
});
