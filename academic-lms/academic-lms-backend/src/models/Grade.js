const mongoose = require('mongoose');

// Grade (e.g. Grade 6, Grade 10, Grade 12)
const gradeSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },          // "Grade 6"
    level: { type: Number, required: true },         // 6
    division: {
      type: String,
      enum: ['primary', 'junior_secondary', 'senior_secondary', 'al'],
      required: true,
    },
    academicYear: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'AcademicYear',
      required: true,
    },
    sectionalHead: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  },
  { timestamps: true }
);

// Section/Class within a grade (e.g. Grade 6A, 6B)
const sectionSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },          // "A", "B", "Science"
    grade: { type: mongoose.Schema.Types.ObjectId, ref: 'Grade', required: true },
    stream: { type: mongoose.Schema.Types.ObjectId, ref: 'Stream' },
    classTeacher: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
    capacity: { type: Number, default: 40 },
    room: { type: String },
    academicYear: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'AcademicYear',
      required: true,
    },
  },
  { timestamps: true }
);

const Grade = mongoose.model('Grade', gradeSchema);
const Section = mongoose.model('Section', sectionSchema);

module.exports = { Grade, Section };
