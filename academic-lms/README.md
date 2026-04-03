# 🎓 Academic Management Service — LMS

A full-stack **React + Node.js + MongoDB** application for Sri Lankan school Academic Management, built as a microservice.

---

## 📁 Project Structure

```
academic-lms/
├── backend/                  ← Node.js / Express API
│   └── src/
│       ├── config/
│       │   ├── db.js         ← MongoDB connection
│       │   └── seed.js       ← Sample data seeder
│       ├── models/
│       │   ├── User.js
│       │   ├── AcademicYear.js
│       │   ├── Grade.js      ← Grade + Section models
│       │   ├── Stream.js     ← A/L streams (Science, Arts...)
│       │   ├── Subject.js
│       │   ├── TeacherAssignment.js
│       │   ├── StudentEnrollment.js
│       │   └── TimetableSlot.js
│       ├── controllers/
│       │   ├── authController.js
│       │   ├── academicYearController.js
│       │   ├── gradeController.js
│       │   ├── subjectController.js
│       │   ├── enrollmentController.js
│       │   ├── teacherAssignmentController.js
│       │   └── timetableController.js
│       ├── routes/
│       │   └── index.js      ← All API routes
│       ├── middleware/
│       │   └── auth.js       ← JWT protect + role authorize
│       ├── events/
│       │   ├── eventBus.js   ← Internal event emitter
│       │   └── academicEvents.js ← Publish & consume domain events
│       └── server.js         ← Express app entry point
│
└── frontend/                 ← React app
    └── src/
        ├── services/
        │   └── api.js        ← All Axios API calls
        ├── context/
        │   └── AuthContext.js
        ├── components/
        │   └── layout/
        │       └── Layout.js ← Sidebar + topbar shell
        ├── pages/
        │   ├── LoginPage.js
        │   ├── DashboardPage.js
        │   ├── GradesPage.js
        │   ├── StudentsPage.js
        │   ├── TeachersPage.js
        │   ├── SubjectsPage.js
        │   └── TimetablePage.js
        ├── App.js
        ├── index.js
        └── index.css
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js v18+
- MongoDB (local or Atlas)

---

### 1. Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env — set your MONGODB_URI and JWT_SECRET
npm install
npm run dev
```

**Seed sample data (Sri Lankan school):**
```bash
npm run seed
```

Demo accounts after seeding:
| Role      | Email                    | Password     |
|-----------|--------------------------|--------------|
| Admin     | admin@school.lk          | password123  |
| Principal | principal@school.lk      | password123  |
| Teacher   | teacher1@school.lk       | password123  |
| Student   | student1@school.lk       | password123  |

---

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000)

---

## 📡 API Endpoints

| Method | Endpoint                              | Description                  | Auth        |
|--------|---------------------------------------|------------------------------|-------------|
| POST   | /api/auth/login                       | Login                        | Public      |
| GET    | /api/auth/me                          | Get current user             | Protected   |
| GET    | /api/academic-years                   | List all academic years      | Protected   |
| GET    | /api/academic-years/active            | Get active year              | Protected   |
| POST   | /api/academic-years                   | Create academic year         | Admin       |
| PATCH  | /api/academic-years/:id/activate      | Set active year              | Admin       |
| GET    | /api/grades                           | List grades                  | Protected   |
| POST   | /api/grades                           | Create grade                 | Admin       |
| GET    | /api/sections                         | List sections/classes        | Protected   |
| POST   | /api/sections                         | Create section               | Admin       |
| GET    | /api/subjects                         | List subjects                | Protected   |
| POST   | /api/subjects                         | Create subject               | Admin       |
| GET    | /api/enrollments                      | List student enrollments     | Staff       |
| POST   | /api/enrollments                      | Enroll a student             | Admin       |
| PATCH  | /api/enrollments/:id/transfer         | Transfer student             | Admin       |
| POST   | /api/enrollments/promote              | Bulk promote students        | Admin       |
| GET    | /api/teacher-assignments              | List teacher assignments     | Staff       |
| POST   | /api/teacher-assignments              | Assign teacher to subject    | Admin       |
| GET    | /api/timetable                        | Get timetable slots          | Protected   |
| POST   | /api/timetable                        | Add a slot                   | Admin       |
| POST   | /api/timetable/publish                | Publish timetable            | Admin       |

---

## 📡 Domain Events

### Published
| Event                           | Trigger                        |
|---------------------------------|-------------------------------|
| `academic.class.created`        | New section/class created     |
| `academic.student.enrolled`     | Student enrolled in a class   |
| `academic.teacher.assigned`     | Teacher assigned to subject   |
| `academic.timetable.published`  | Timetable published           |

### Consumed
| Event                        | Action                        |
|------------------------------|-------------------------------|
| `identity.user.created`      | Sync new user to academic DB  |
| `identity.user.role.updated` | Update user role locally      |

---

## 🏫 Sri Lankan School Structure

```
School
└── Academic Year (2024)
    └── Terms (Term 1, Term 2, Term 3)
        └── Grades
            ├── Primary (Grade 1–5)
            ├── Junior Secondary (Grade 6–9)
            ├── Senior Secondary (Grade 10–11) ← O/L
            └── A/L (Grade 12–13)
                └── Streams: Science | Arts | Commerce | Technology
                    └── Sections (A, B, C...)
                        ├── Class Teacher
                        ├── Subject Teachers + Assignments
                        ├── Enrolled Students
                        └── Timetable Slots
```

---

## 🔧 Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | React 18, React Router v6, TanStack Query, Recharts |
| Backend   | Node.js, Express 4                  |
| Database  | MongoDB + Mongoose                  |
| Auth      | JWT (jsonwebtoken + bcryptjs)       |
| Events    | EventEmitter2 (in-process)         |
| Styling   | Custom CSS (dark theme, Sora font)  |
