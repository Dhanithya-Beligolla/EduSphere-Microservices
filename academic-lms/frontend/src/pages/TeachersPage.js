import { useQuery } from '@tanstack/react-query';
import { teacherAssignmentAPI } from '../services/api';

// Mock teacher list – replace with real User API when you add /api/users
const MOCK_TEACHERS = [
  { _id: '1', firstName: 'Kamala', lastName: 'Fernando', employeeId: 'TCH001', email: 'teacher1@school.lk', role: 'subject_teacher', subjects: ['Mathematics'], sections: ['10A', '10B', '11A'] },
  { _id: '2', firstName: 'Sunil', lastName: 'Bandara', employeeId: 'TCH002', email: 'teacher2@school.lk', role: 'class_teacher', subjects: ['Science'], sections: ['9A'] },
  { _id: '3', firstName: 'Priya', lastName: 'Wickramasinghe', employeeId: 'TCH003', email: 'teacher3@school.lk', role: 'subject_teacher', subjects: ['English', 'Sinhala'], sections: ['8A', '8B', '9B'] },
  { _id: '4', firstName: 'Nimal', lastName: 'Dias', employeeId: 'TCH004', email: 'teacher4@school.lk', role: 'sectional_head', subjects: ['History', 'Geography'], sections: ['6A', '6B', '7A', '7B'] },
];

const ROLE_BADGE = {
  subject_teacher: 'badge-blue',
  class_teacher: 'badge-green',
  sectional_head: 'badge-purple',
  principal: 'badge-amber',
};

export default function TeachersPage() {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Teachers</h1>
          <p>Manage teacher roster and teaching assignments</p>
        </div>
        <button className="btn btn-primary">+ Add Teacher</button>
      </div>

      <div className="card">
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Teacher</th>
                <th>Employee ID</th>
                <th>Role</th>
                <th>Subjects</th>
                <th>Sections</th>
                <th>Periods/Week</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {MOCK_TEACHERS.map((t) => (
                <tr key={t._id}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                      <div style={{
                        width: 32, height: 32, borderRadius: '50%',
                        background: 'var(--green-dim)', display: 'flex',
                        alignItems: 'center', justifyContent: 'center',
                        fontSize: '0.78rem', fontWeight: 600, color: 'var(--green)',
                        flexShrink: 0,
                      }}>
                        {t.firstName[0]}{t.lastName[0]}
                      </div>
                      <div>
                        <div style={{ fontWeight: 500, fontSize: '0.88rem' }}>
                          {t.firstName} {t.lastName}
                        </div>
                        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{t.email}</div>
                      </div>
                    </div>
                  </td>
                  <td style={{ fontFamily: 'monospace', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    {t.employeeId}
                  </td>
                  <td>
                    <span className={`badge ${ROLE_BADGE[t.role] || 'badge-blue'}`}>
                      {t.role.replace('_', ' ')}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                      {t.subjects.map((s) => (
                        <span key={s} className="badge badge-amber" style={{ fontSize: '0.66rem' }}>{s}</span>
                      ))}
                    </div>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                      {t.sections.map((s) => (
                        <span key={s} className="badge badge-blue" style={{ fontSize: '0.66rem' }}>{s}</span>
                      ))}
                    </div>
                  </td>
                  <td>
                    <span style={{ color: 'var(--accent)', fontWeight: 600 }}>
                      {t.sections.length * 5}
                    </span>
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}> /wk</span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: 6 }}>
                      <button className="btn btn-ghost btn-sm">Assign</button>
                      <button className="btn btn-ghost btn-sm">Load</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
