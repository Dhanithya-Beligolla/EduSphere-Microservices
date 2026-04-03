const TeacherAssignment = require('../models/TeacherAssignment');
const { publishTeacherAssigned } = require('../events/academicEvents');

// GET /api/teacher-assignments?teacher=&section=&academicYear=
exports.getAssignments = async (req, res) => {
  try {
    const { teacher, section, academicYear } = req.query;
    const filter = {};
    if (teacher) filter.teacher = teacher;
    if (section) filter.section = section;
    if (academicYear) filter.academicYear = academicYear;

    const assignments = await TeacherAssignment.find(filter)
      .populate('teacher', 'firstName lastName email employeeId')
      .populate('subject', 'name code')
      .populate('section', 'name grade')
      .populate('academicYear', 'year');

    res.json({ success: true, data: assignments });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// GET /api/teacher-assignments/teaching-load/:teacherId
exports.getTeachingLoad = async (req, res) => {
  try {
    const assignments = await TeacherAssignment.find({
      teacher: req.params.teacherId,
      isActive: true,
    })
      .populate('subject', 'name code')
      .populate({ path: 'section', populate: { path: 'grade', select: 'name level' } })
      .populate('academicYear', 'year');

    const totalPeriods = assignments.reduce((sum, a) => sum + a.periodsPerWeek, 0);
    res.json({ success: true, totalPeriods, data: assignments });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// POST /api/teacher-assignments
exports.createAssignment = async (req, res) => {
  try {
    const assignment = await TeacherAssignment.create(req.body);

    publishTeacherAssigned({
      teacherId: assignment.teacher,
      subjectId: assignment.subject,
      sectionId: assignment.section,
      academicYearId: assignment.academicYear,
    });

    const populated = await assignment.populate([
      { path: 'teacher', select: 'firstName lastName' },
      { path: 'subject', select: 'name code' },
      { path: 'section', select: 'name' },
    ]);

    res.status(201).json({ success: true, data: populated });
  } catch (err) {
    if (err.code === 11000) {
      return res.status(400).json({
        success: false,
        message: 'This teacher is already assigned to this subject in this section',
      });
    }
    res.status(400).json({ success: false, message: err.message });
  }
};

// DELETE /api/teacher-assignments/:id
exports.removeAssignment = async (req, res) => {
  try {
    await TeacherAssignment.findByIdAndDelete(req.params.id);
    res.json({ success: true, message: 'Assignment removed' });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};
