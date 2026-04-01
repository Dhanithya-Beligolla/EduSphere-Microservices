const TimetableSlot = require('../models/TimetableSlot');
const { publishTimetablePublished } = require('../events/academicEvents');

// GET /api/timetable?section=&teacher=&academicYear=
exports.getTimetable = async (req, res) => {
  try {
    const { section, teacher, academicYear } = req.query;
    const filter = {};
    if (section) filter.section = section;
    if (teacher) filter.teacher = teacher;
    if (academicYear) filter.academicYear = academicYear;

    const slots = await TimetableSlot.find(filter)
      .populate('subject', 'name code')
      .populate('teacher', 'firstName lastName')
      .populate('section', 'name')
      .sort({ dayOfWeek: 1, periodNumber: 1 });

    res.json({ success: true, data: slots });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// POST /api/timetable
exports.createSlot = async (req, res) => {
  try {
    const slot = await TimetableSlot.create(req.body);
    res.status(201).json({ success: true, data: slot });
  } catch (err) {
    if (err.code === 11000) {
      return res.status(400).json({
        success: false,
        message: 'This time slot is already occupied (teacher or section conflict)',
      });
    }
    res.status(400).json({ success: false, message: err.message });
  }
};

// POST /api/timetable/bulk
exports.createBulkSlots = async (req, res) => {
  try {
    const { slots } = req.body;
    const created = await TimetableSlot.insertMany(slots, { ordered: false });
    res.status(201).json({ success: true, count: created.length, data: created });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

// PATCH /api/timetable/:id
exports.updateSlot = async (req, res) => {
  try {
    const slot = await TimetableSlot.findByIdAndUpdate(req.params.id, req.body, { new: true });
    res.json({ success: true, data: slot });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

// DELETE /api/timetable/:id
exports.deleteSlot = async (req, res) => {
  try {
    await TimetableSlot.findByIdAndDelete(req.params.id);
    res.json({ success: true, message: 'Slot deleted' });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// POST /api/timetable/publish
exports.publishTimetable = async (req, res) => {
  try {
    const { sectionId, academicYearId } = req.body;
    const result = await TimetableSlot.updateMany(
      { section: sectionId, academicYear: academicYearId },
      { isPublished: true }
    );

    publishTimetablePublished({ sectionId, academicYearId, slotsPublished: result.modifiedCount });

    res.json({ success: true, published: result.modifiedCount });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};
