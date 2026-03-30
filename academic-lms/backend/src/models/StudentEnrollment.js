const mongoose = require('mongoose');

const studentEnrollmentSchema = new mongoose.Schema(
  {
    student: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    section: { type: mongoose.Schema.Types.ObjectId, ref: 'Section', required: true },
    grade: { type: mongoose.Schema.Types.ObjectId, ref: 'Grade', required: true },
    academicYear: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'AcademicYear',
      required: true,
    },
    rollNumber: { type: String },
    admissionNumber: { type: String, unique: true },
    status: {
      type: String,
      enum: ['active', 'transferred', 'promoted', 'withdrawn'],
      default: 'active',
    },
    enrolledDate: { type: Date, default: Date.now },
    subjects: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Subject' }],
    previousSection: { type: mongoose.Schema.Types.ObjectId, ref: 'Section' }, // for transfers
  },
  { timestamps: true }
);

studentEnrollmentSchema.index(
  { student: 1, academicYear: 1 },
  { unique: true }
);

module.exports = mongoose.model('StudentEnrollment', studentEnrollmentSchema);
