const Subject = require('../models/Subject');

exports.getSubjects = async (req, res) => {
  try {
    const { grade, medium, type } = req.query;
    const filter = {};
    if (grade) filter.applicableGrades = Number(grade);
    if (medium) filter.medium = medium;
    if (type) filter.type = type;
    const subjects = await Subject.find(filter).sort({ name: 1 });
    res.json({ success: true, data: subjects });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

exports.getSubject = async (req, res) => {
  try {
    const subject = await Subject.findById(req.params.id);
    if (!subject) return res.status(404).json({ success: false, message: 'Subject not found' });
    res.json({ success: true, data: subject });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

exports.createSubject = async (req, res) => {
  try {
    const subject = await Subject.create(req.body);
    res.status(201).json({ success: true, data: subject });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

exports.updateSubject = async (req, res) => {
  try {
    const subject = await Subject.findByIdAndUpdate(req.params.id, req.body, { new: true });
    res.json({ success: true, data: subject });
  } catch (err) {
    res.status(400).json({ success: false, message: err.message });
  }
};

exports.deleteSubject = async (req, res) => {
  try {
    await Subject.findByIdAndDelete(req.params.id);
    res.json({ success: true, message: 'Subject deleted' });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};
