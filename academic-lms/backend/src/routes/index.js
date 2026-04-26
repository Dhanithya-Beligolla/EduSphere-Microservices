const express = require('express');
const router = express.Router();

const gradeController = require('../controllers/gradeController');
const academicYearController = require('../controllers/academicYearController');
const subjectController = require('../controllers/subjectController');
const enrollmentController = require('../controllers/enrollmentController');
const teacherAssignmentController = require('../controllers/teacherAssignmentController');
const timetableController = require('../controllers/timetableController');

/**
 * @swagger
 * tags:
 *   - name: Academic Years
 *   - name: Grades
 *   - name: Sections
 *   - name: Subjects
 *   - name: Enrollments
 *   - name: Teacher Assignments
 *   - name: Timetable
 */

/**
 * @swagger
 * /academic-years:
 *   get:
 *     summary: Get all academic years
 *     tags: [Academic Years]
 *     responses:
 *       200:
 *         description: List of academic years
 */
router.get('/academic-years', academicYearController.getAll);

/**
 * @swagger
 * /academic-years/active:
 *   get:
 *     summary: Get active academic year
 *     tags: [Academic Years]
 *     responses:
 *       200:
 *         description: Active academic year
 */
router.get('/academic-years/active', academicYearController.getActive);

/**
 * @swagger
 * /academic-years:
 *   post:
 *     summary: Create a new academic year
 *     tags: [Academic Years]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       201:
 *         description: Academic year created
 */
router.post('/academic-years', academicYearController.create);

/**
 * @swagger
 * /academic-years/{id}/activate:
 *   patch:
 *     summary: Activate an academic year
 *     tags: [Academic Years]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Academic year activated
 */
router.patch('/academic-years/:id/activate', academicYearController.activate);

/**
 * @swagger
 * /academic-years/{id}:
 *   delete:
 *     summary: Delete an academic year
 *     tags: [Academic Years]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Academic year deleted
 */
router.delete('/academic-years/:id', academicYearController.remove);

/**
 * @swagger
 * /grades:
 *   get:
 *     summary: Get all grades
 *     tags: [Grades]
 *     responses:
 *       200:
 *         description: List of grades
 */
router.get('/grades', gradeController.getGrades);

/**
 * @swagger
 * /grades:
 *   post:
 *     summary: Create a new grade
 *     tags: [Grades]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       201:
 *         description: Grade created
 */
router.post('/grades', gradeController.createGrade);

/**
 * @swagger
 * /grades/{id}:
 *   put:
 *     summary: Update a grade
 *     tags: [Grades]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       200:
 *         description: Grade updated
 */
router.put('/grades/:id', gradeController.updateGrade);

/**
 * @swagger
 * /grades/{id}:
 *   delete:
 *     summary: Delete a grade
 *     tags: [Grades]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Grade deleted
 */
router.delete('/grades/:id', gradeController.deleteGrade);

/**
 * @swagger
 * /sections:
 *   get:
 *     summary: Get all sections
 *     tags: [Sections]
 *     responses:
 *       200:
 *         description: List of sections
 */
router.get('/sections', gradeController.getSections);

/**
 * @swagger
 * /sections:
 *   post:
 *     summary: Create a new section
 *     tags: [Sections]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       201:
 *         description: Section created
 */
router.post('/sections', gradeController.createSection);

/**
 * @swagger
 * /sections/{id}:
 *   put:
 *     summary: Update a section
 *     tags: [Sections]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       200:
 *         description: Section updated
 */
router.put('/sections/:id', gradeController.updateSection);

/**
 * @swagger
 * /sections/{id}:
 *   delete:
 *     summary: Delete a section
 *     tags: [Sections]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Section deleted
 */
router.delete('/sections/:id', gradeController.deleteSection);

/**
 * @swagger
 * /subjects:
 *   get:
 *     summary: Get all subjects
 *     tags: [Subjects]
 *     responses:
 *       200:
 *         description: List of subjects
 */
router.get('/subjects', subjectController.getSubjects);

/**
 * @swagger
 * /subjects/{id}:
 *   get:
 *     summary: Get a subject by ID
 *     tags: [Subjects]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Subject details
 */
router.get('/subjects/:id', subjectController.getSubject);

/**
 * @swagger
 * /subjects:
 *   post:
 *     summary: Create a new subject
 *     tags: [Subjects]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       201:
 *         description: Subject created
 */
router.post('/subjects', subjectController.createSubject);

/**
 * @swagger
 * /subjects/{id}:
 *   put:
 *     summary: Update a subject
 *     tags: [Subjects]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       200:
 *         description: Subject updated
 */
router.put('/subjects/:id', subjectController.updateSubject);

/**
 * @swagger
 * /subjects/{id}:
 *   delete:
 *     summary: Delete a subject
 *     tags: [Subjects]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Subject deleted
 */
router.delete('/subjects/:id', subjectController.deleteSubject);

/**
 * @swagger
 * /enrollments:
 *   get:
 *     summary: Get all enrollments
 *     tags: [Enrollments]
 *     responses:
 *       200:
 *         description: List of enrollments
 */
router.get('/enrollments', enrollmentController.getEnrollments);

/**
 * @swagger
 * /enrollments/student/{studentId}:
 *   get:
 *     summary: Get a student's enrollment
 *     tags: [Enrollments]
 *     parameters:
 *       - in: path
 *         name: studentId
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Student enrollment details
 */
router.get('/enrollments/student/:studentId', enrollmentController.getStudentEnrollment);

/**
 * @swagger
 * /enrollments:
 *   post:
 *     summary: Enroll a student
 *     tags: [Enrollments]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       201:
 *         description: Student enrolled
 */
router.post('/enrollments', enrollmentController.enrollStudent);

/**
 * @swagger
 * /enrollments/{id}/transfer:
 *   patch:
 *     summary: Transfer a student enrollment
 *     tags: [Enrollments]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: false
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       200:
 *         description: Student transferred
 */
router.patch('/enrollments/:id/transfer', enrollmentController.transferStudent);

/**
 * @swagger
 * /enrollments/promote:
 *   post:
 *     summary: Promote students
 *     tags: [Enrollments]
 *     requestBody:
 *       required: false
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       200:
 *         description: Students promoted
 */
router.post('/enrollments/promote', enrollmentController.promoteStudents);

/**
 * @swagger
 * /teacher-assignments:
 *   get:
 *     summary: Get all teacher assignments
 *     tags: [Teacher Assignments]
 *     responses:
 *       200:
 *         description: List of teacher assignments
 */
router.get('/teacher-assignments', teacherAssignmentController.getAssignments);

/**
 * @swagger
 * /teacher-assignments/teaching-load/{teacherId}:
 *   get:
 *     summary: Get teaching load for a teacher
 *     tags: [Teacher Assignments]
 *     parameters:
 *       - in: path
 *         name: teacherId
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Teaching load details
 */
router.get('/teacher-assignments/teaching-load/:teacherId', teacherAssignmentController.getTeachingLoad);

/**
 * @swagger
 * /teacher-assignments:
 *   post:
 *     summary: Create a teacher assignment
 *     tags: [Teacher Assignments]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       201:
 *         description: Teacher assignment created
 */
router.post('/teacher-assignments', teacherAssignmentController.createAssignment);

/**
 * @swagger
 * /teacher-assignments/{id}:
 *   delete:
 *     summary: Delete a teacher assignment
 *     tags: [Teacher Assignments]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Teacher assignment deleted
 */
router.delete('/teacher-assignments/:id', teacherAssignmentController.removeAssignment);

/**
 * @swagger
 * /timetable:
 *   get:
 *     summary: Get timetable
 *     tags: [Timetable]
 *     responses:
 *       200:
 *         description: Timetable data
 */
router.get('/timetable', timetableController.getTimetable);

/**
 * @swagger
 * /timetable:
 *   post:
 *     summary: Create a timetable slot
 *     tags: [Timetable]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       201:
 *         description: Timetable slot created
 */
router.post('/timetable', timetableController.createSlot);

/**
 * @swagger
 * /timetable/bulk:
 *   post:
 *     summary: Create timetable slots in bulk
 *     tags: [Timetable]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       201:
 *         description: Bulk timetable slots created
 */
router.post('/timetable/bulk', timetableController.createBulkSlots);

/**
 * @swagger
 * /timetable/{id}:
 *   put:
 *     summary: Update a timetable slot
 *     tags: [Timetable]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       200:
 *         description: Timetable slot updated
 */
router.put('/timetable/:id', timetableController.updateSlot);

/**
 * @swagger
 * /timetable/{id}:
 *   delete:
 *     summary: Delete a timetable slot
 *     tags: [Timetable]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Timetable slot deleted
 */
router.delete('/timetable/:id', timetableController.deleteSlot);

/**
 * @swagger
 * /timetable/publish:
 *   post:
 *     summary: Publish timetable
 *     tags: [Timetable]
 *     responses:
 *       200:
 *         description: Timetable published
 */
router.post('/timetable/publish', timetableController.publishTimetable);

module.exports = router;