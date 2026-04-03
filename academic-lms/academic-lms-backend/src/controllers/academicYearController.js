const AcademicYear = require('../models/AcademicYear');

// GET /api/academic-years
exports.getAll = async (req, res) => {
  try {
    const years = await AcademicYear.find().sort({ year: -1 });
    res.json({ success: true, data: years });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// GET /api/academic-years/active
exports.getActive = async (req, res) => {
  try {
    const year = await AcademicYear.findOne({ isActive: true });
    if (!year) return res.status(404).json({ success: false, message: 'No active academic year' });
    res.json({ success: true, data: year });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// POST /api/academic-years
exports.create = async (req, res) => {
  try {
    const { year, startDate, endDate, terms } = req.body;
    const academicYear = await AcademicYear.create({
      year, startDate, endDate, terms,
      createdBy: req.user._id,
    });
    res.status(201).json({ success: true, data: academicYear });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

// PATCH /api/academic-years/:id/activate
exports.activate = async (req, res) => {
  try {
    // Deactivate all first
    await AcademicYear.updateMany({}, { isActive: false });
    const year = await AcademicYear.findByIdAndUpdate(
      req.params.id,
      { isActive: true },
      { new: true }
    );
    res.json({ success: true, data: year });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// DELETE /api/academic-years/:id
exports.remove = async (req, res) => {
  try {
    await AcademicYear.findByIdAndDelete(req.params.id);
    res.json({ success: true, message: 'Academic year deleted' });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};
