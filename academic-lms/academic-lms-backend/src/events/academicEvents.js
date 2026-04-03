const eventBus = require('./eventBus');

// ─── PUBLISHERS ──────────────────────────────────────────────────────────────

const publishClassCreated = (classData) => {
  eventBus.emit('academic.class.created', {
    event: 'academic.class.created',
    timestamp: new Date().toISOString(),
    payload: classData,
  });
};

const publishStudentEnrolled = (enrollmentData) => {
  eventBus.emit('academic.student.enrolled', {
    event: 'academic.student.enrolled',
    timestamp: new Date().toISOString(),
    payload: enrollmentData,
  });
};

const publishTeacherAssigned = (assignmentData) => {
  eventBus.emit('academic.teacher.assigned', {
    event: 'academic.teacher.assigned',
    timestamp: new Date().toISOString(),
    payload: assignmentData,
  });
};

const publishTimetablePublished = (timetableData) => {
  eventBus.emit('academic.timetable.published', {
    event: 'academic.timetable.published',
    timestamp: new Date().toISOString(),
    payload: timetableData,
  });
};

// ─── CONSUMERS ───────────────────────────────────────────────────────────────

const registerEventListeners = () => {
  // When identity service creates a user
  eventBus.on('identity.user.created', async (data) => {
    console.log('📥 [Consumer] identity.user.created:', data.payload);
    // Sync new user to local User collection if needed
  });

  // When a user's role is updated in identity service
  eventBus.on('identity.user.role.updated', async (data) => {
    console.log('📥 [Consumer] identity.user.role.updated:', data.payload);
    // Update user role in academic service
  });
};

module.exports = {
  publishClassCreated,
  publishStudentEnrolled,
  publishTeacherAssigned,
  publishTimetablePublished,
  registerEventListeners,
};
