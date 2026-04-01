const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema(
  {
    firstName: { type: String, required: true, trim: true },
    lastName: { type: String, required: true, trim: true },
    email: { type: String, required: true, unique: true, lowercase: true },
    password: { type: String, required: true, select: false },
    role: {
      type: String,
      enum: ['admin', 'principal', 'sectional_head', 'class_teacher', 'subject_teacher', 'student'],
      required: true,
    },
    phone: { type: String },
    gender: { type: String, enum: ['male', 'female', 'other'] },
    dateOfBirth: { type: Date },
    address: { type: String },
    profileImage: { type: String },
    nic: { type: String },                              // National ID
    isActive: { type: Boolean, default: true },
    // Teacher-specific
    employeeId: { type: String },
    qualifications: [{ type: String }],
    joinedDate: { type: Date },
    // Student-specific
    parentName: { type: String },
    parentPhone: { type: String },
    parentEmail: { type: String },
  },
  { timestamps: true }
);

// Hash password before saving
userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

userSchema.methods.comparePassword = async function (candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

userSchema.virtual('fullName').get(function () {
  return `${this.firstName} ${this.lastName}`;
});

module.exports = mongoose.model('User', userSchema);
