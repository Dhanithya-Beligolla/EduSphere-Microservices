import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
});

// ─── ACADEMIC YEARS ────────────────────────────────────────────────────────────
export const academicYearAPI = {
  getAll: () => api.get('/academic-years'),
  getActive: () => api.get('/academic-years/active'),
  create: (data) => api.post('/academic-years', data),
  activate: (id) => api.patch(`/academic-years/${id}/activate`),
  remove: (id) => api.delete(`/academic-years/${id}`),
};

// ─── GRADES ────────────────────────────────────────────────────────────────────
export const gradeAPI = {
  getAll: (params) => api.get('/grades', { params }),
  create: (data) => api.post('/grades', data),
  update: (id, data) => api.put(`/grades/${id}`, data),
  remove: (id) => api.delete(`/grades/${id}`),
};

// ─── SECTIONS ──────────────────────────────────────────────────────────────────
export const sectionAPI = {
  getAll: (params) => api.get('/sections', { params }),
  create: (data) => api.post('/sections', data),
  update: (id, data) => api.put(`/sections/${id}`, data),
  remove: (id) => api.delete(`/sections/${id}`),
};

// ─── SUBJECTS ──────────────────────────────────────────────────────────────────
export const subjectAPI = {
  getAll: (params) => api.get('/subjects', { params }),
  getOne: (id) => api.get(`/subjects/${id}`),
  create: (data) => api.post('/subjects', data),
  update: (id, data) => api.put(`/subjects/${id}`, data),
  remove: (id) => api.delete(`/subjects/${id}`),
};

// ─── ENROLLMENTS ───────────────────────────────────────────────────────────────
export const enrollmentAPI = {
  getAll: (params) => api.get('/enrollments', { params }),
  getByStudent: (studentId) => api.get(`/enrollments/student/${studentId}`),
  enroll: (data) => api.post('/enrollments', data),
  transfer: (id, data) => api.patch(`/enrollments/${id}/transfer`, data),
  promote: (data) => api.post('/enrollments/promote', data),
};

// ─── TEACHER ASSIGNMENTS ───────────────────────────────────────────────────────
export const teacherAssignmentAPI = {
  getAll: (params) => api.get('/teacher-assignments', { params }),
  getTeachingLoad: (teacherId) => api.get(`/teacher-assignments/teaching-load/${teacherId}`),
  create: (data) => api.post('/teacher-assignments', data),
  remove: (id) => api.delete(`/teacher-assignments/${id}`),
};

// ─── TIMETABLE ─────────────────────────────────────────────────────────────────
export const timetableAPI = {
  get: (params) => api.get('/timetable', { params }),
  createSlot: (data) => api.post('/timetable', data),
  createBulk: (slots) => api.post('/timetable/bulk', { slots }),
  update: (id, data) => api.put(`/timetable/${id}`, data),
  remove: (id) => api.delete(`/timetable/${id}`),
  publish: (data) => api.post('/timetable/publish', data),
};

export default api;
