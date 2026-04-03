const mongoose = require('mongoose');

const timetableSlotSchema = new mongoose.Schema(
  {
    section: { type: mongoose.Schema.Types.ObjectId, ref: 'Section', required: true },
    subject: { type: mongoose.Schema.Types.ObjectId, ref: 'Subject', required: true },
    teacher: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    academicYear: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'AcademicYear',
      required: true,
    },
    term: { type: String },
    dayOfWeek: {
      type: Number,
      required: true,
      min: 1,
      max: 5, // 1=Mon ... 5=Fri
    },
    periodNumber: { type: Number, required: true },  // 1–8
    startTime: { type: String, required: true },      // "08:00"
    endTime: { type: String, required: true },        // "08:45"
    room: { type: String },
    isPublished: { type: Boolean, default: false },
  },
  { timestamps: true }
);

// No teacher double-booking
timetableSlotSchema.index(
  { teacher: 1, dayOfWeek: 1, periodNumber: 1, academicYear: 1 },
  { unique: true }
);

// No section double-booking
timetableSlotSchema.index(
  { section: 1, dayOfWeek: 1, periodNumber: 1, academicYear: 1 },
  { unique: true }
);

module.exports = mongoose.model('TimetableSlot', timetableSlotSchema);
