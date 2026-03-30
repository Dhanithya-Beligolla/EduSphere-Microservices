const { Grade, Section } = require('../models/Grade');
const { publishClassCreated } = require('../events/academicEvents');

// ─── GRADES ──────────────────────────────────────────────────────────────────

exports.getGrades = async (req, res) => {
  try {
    const { academicYear } = req.query;
    const filter = academicYear ? { academicYear } : {};
    const grades = await Grade.find(filter)
      .populate('academicYear', 'year')
      .populate('sectionalHead', 'firstName lastName email')
      .sort({ level: 1 });
    res.json({ success: true, data: grades });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

exports.createGrade = async (req, res) => {
  try {
    const grade = await Grade.create(req.body);
    res.status(201).json({ success: true, data: grade });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

exports.updateGrade = async (req, res) => {
  try {
    const grade = await Grade.findByIdAndUpdate(req.params.id, req.body, { new: true });
    res.json({ success: true, data: grade });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

exports.deleteGrade = async (req, res) => {
  try {
    await Grade.findByIdAndDelete(req.params.id);
    res.json({ success: true, message: 'Grade deleted' });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// ─── SECTIONS ────────────────────────────────────────────────────────────────

exports.getSections = async (req, res) => {
  try {
    const { grade, academicYear } = req.query;
    const filter = {};
    if (grade) filter.grade = grade;
    if (academicYear) filter.academicYear = academicYear;

    const sections = await Section.find(filter)
      .populate('grade', 'name level division')
      .populate('stream', 'name code')
      .populate('classTeacher', 'firstName lastName email')
      .populate('academicYear', 'year');
    res.json({ success: true, data: sections });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

exports.createSection = async (req, res) => {
  try {
    const section = await Section.create(req.body);
    const populated = await section.populate([
      { path: 'grade', select: 'name level' },
      { path: 'classTeacher', select: 'firstName lastName' },
    ]);

    // Publish domain event
    publishClassCreated({
      sectionId: section._id,
      sectionName: section.name,
      gradeId: section.grade,
      academicYearId: section.academicYear,
    });

    res.status(201).json({ success: true, data: populated });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

exports.updateSection = async (req, res) => {
  try {
    const section = await Section.findByIdAndUpdate(req.params.id, req.body, { new: true })
      .populate('grade', 'name level')
      .populate('classTeacher', 'firstName lastName');
    res.json({ success: true, data: section });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

exports.deleteSection = async (req, res) => {
  try {
    await Section.findByIdAndDelete(req.params.id);
    res.json({ success: true, message: 'Section deleted' });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};
