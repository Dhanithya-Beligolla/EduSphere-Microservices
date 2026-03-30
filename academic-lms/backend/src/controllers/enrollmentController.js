const StudentEnrollment = require('../models/StudentEnrollment');
const { publishStudentEnrolled } = require('../events/academicEvents');

// GET /api/enrollments?section=&academicYear=&status=
exports.getEnrollments = async (req, res) => {
  try {
    const { section, academicYear, status, grade } = req.query;
    const filter = {};
    if (section) filter.section = section;
    if (academicYear) filter.academicYear = academicYear;
    if (status) filter.status = status;
    if (grade) filter.grade = grade;

    const enrollments = await StudentEnrollment.find(filter)
      .populate('student', 'firstName lastName email admissionNumber profileImage')
      .populate('section', 'name')
      .populate('grade', 'name level')
      .populate('academicYear', 'year')
      .sort({ rollNumber: 1 });

    res.json({ success: true, count: enrollments.length, data: enrollments });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// GET /api/enrollments/student/:studentId
exports.getStudentEnrollment = async (req, res) => {
  try {
    const enrollment = await StudentEnrollment.findOne({
      student: req.params.studentId,
    })
      .populate('student', 'firstName lastName email')
      .populate('section grade academicYear subjects');
    if (!enrollment) return res.status(404).json({ success: false, message: 'Enrollment not found' });
    res.json({ success: true, data: enrollment });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// POST /api/enrollments
exports.enrollStudent = async (req, res) => {
  try {
    const enrollment = await StudentEnrollment.create(req.body);

    publishStudentEnrolled({
      studentId: enrollment.student,
      sectionId: enrollment.section,
      gradeId: enrollment.grade,
      academicYearId: enrollment.academicYear,
      admissionNumber: enrollment.admissionNumber,
    });

    res.status(201).json({ success: true, data: enrollment });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

// PATCH /api/enrollments/:id/transfer
exports.transferStudent = async (req, res) => {
  try {
    const { newSection } = req.body;
    const enrollment = await StudentEnrollment.findById(req.params.id);
    if (!enrollment) return res.status(404).json({ success: false, message: 'Enrollment not found' });

    enrollment.previousSection = enrollment.section;
    enrollment.section = newSection;
    enrollment.status = 'transferred';
    await enrollment.save();

    res.json({ success: true, data: enrollment });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

// POST /api/enrollments/promote  — bulk promote at year-end
exports.promoteStudents = async (req, res) => {
  try {
    const { academicYearId, gradeId } = req.body;
    const result = await StudentEnrollment.updateMany(
      { academicYear: academicYearId, grade: gradeId, status: 'active' },
      { status: 'promoted' }
    );
    res.json({ success: true, promoted: result.modifiedCount });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};
