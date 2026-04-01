const mongoose = require('mongoose');

const termSchema = new mongoose.Schema({
  name: { type: String, required: true },        // e.g. "Term 1"
  startDate: { type: Date, required: true },
  endDate: { type: Date, required: true },
  isActive: { type: Boolean, default: false },
});

const academicYearSchema = new mongoose.Schema(
  {
    year: { type: String, required: true, unique: true }, // e.g. "2024"
    startDate: { type: Date, required: true },
    endDate: { type: Date, required: true },
    terms: [termSchema],
    isActive: { type: Boolean, default: false },
    createdBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  },
  { timestamps: true }
);

module.exports = mongoose.model('AcademicYear', academicYearSchema);
