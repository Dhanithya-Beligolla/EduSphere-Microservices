const mongoose = require('mongoose');

const subjectSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },            // "Mathematics"
    code: { type: String, required: true, unique: true }, // "MATH"
    description: { type: String },
    type: {
      type: String,
      enum: ['core', 'optional', 'extra_curricular'],
      default: 'core',
    },
    periodsPerWeek: { type: Number, default: 5 },
    applicableGrades: [{ type: Number }],              // [6,7,8,9,10]
    medium: {
      type: String,
      enum: ['sinhala', 'tamil', 'english'],
      default: 'sinhala',
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Subject', subjectSchema);
