const express = require('express');
const router = express.Router();

const gradeController = require('../controllers/gradeController');
const academicYearController = require('../controllers/academicYearController');
const subjectController = require('../controllers/subjectController');
const enrollmentController = require('../controllers/enrollmentController');
const teacherAssignmentController = require('../controllers/teacherAssignmentController');
const timetableController = require('../controllers/timetableController');

// ─── ACADEMIC YEARS ───────────────────────────────────────────────────────────
router.get('/academic-years', academicYearController.getAll);
router.get('/academic-years/active', academicYearController.getActive);
router.post('/academic-years', academicYearController.create);
router.patch('/academic-years/:id/activate', academicYearController.activate);
router.delete('/academic-years/:id', academicYearController.remove);

// ─── GRADES ───────────────────────────────────────────────────────────────────
router.get('/grades', gradeController.getGrades);
router.post('/grades', gradeController.createGrade);
router.put('/grades/:id', gradeController.updateGrade);
router.delete('/grades/:id', gradeController.deleteGrade);

// ─── SECTIONS ─────────────────────────────────────────────────────────────────
router.get('/sections', gradeController.getSections);
router.post('/sections', gradeController.createSection);
router.put('/sections/:id', gradeController.updateSection);
router.delete('/sections/:id', gradeController.deleteSection);

// ─── SUBJECTS ─────────────────────────────────────────────────────────────────
router.get('/subjects', subjectController.getSubjects);
router.get('/subjects/:id', subjectController.getSubject);
router.post('/subjects', subjectController.createSubject);
router.put('/subjects/:id', subjectController.updateSubject);
router.delete('/subjects/:id', subjectController.deleteSubject);

// ─── ENROLLMENTS ──────────────────────────────────────────────────────────────
router.get('/enrollments', enrollmentController.getEnrollments);
router.get('/enrollments/student/:studentId', enrollmentController.getStudentEnrollment);
router.post('/enrollments', enrollmentController.enrollStudent);
router.patch('/enrollments/:id/transfer', enrollmentController.transferStudent);
router.post('/enrollments/promote', enrollmentController.promoteStudents);

// ─── TEACHER ASSIGNMENTS ──────────────────────────────────────────────────────
router.get('/teacher-assignments', teacherAssignmentController.getAssignments);
router.get('/teacher-assignments/teaching-load/:teacherId', teacherAssignmentController.getTeachingLoad);
router.post('/teacher-assignments', teacherAssignmentController.createAssignment);
router.delete('/teacher-assignments/:id', teacherAssignmentController.removeAssignment);

// ─── TIMETABLE ────────────────────────────────────────────────────────────────
router.get('/timetable', timetableController.getTimetable);
router.post('/timetable', timetableController.createSlot);
router.post('/timetable/bulk', timetableController.createBulkSlots);
router.put('/timetable/:id', timetableController.updateSlot);
router.delete('/timetable/:id', timetableController.deleteSlot);
router.post('/timetable/publish', timetableController.publishTimetable);

module.exports = router;
