const mongoose = require('mongoose');

const streamSchema = new mongoose.Schema(
  {
    name: { type: String, required: true },   // "Science", "Arts", "Commerce", "Technology"
    code: { type: String, required: true, unique: true },  // "SCI", "ART", "COM"
    description: { type: String },
    applicableGrades: [{ type: Number }],     // [12, 13] for A/L
    subjects: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Subject' }],
  },
  { timestamps: true }
);

module.exports = mongoose.model('Stream', streamSchema);
