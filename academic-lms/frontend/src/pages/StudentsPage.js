import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { enrollmentAPI } from '../services/api';

const STATUS_BADGE = {
  active: 'badge-green',
  transferred: 'badge-amber',
  promoted: 'badge-blue',
  withdrawn: 'badge-red',
};

export default function StudentsPage() {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('active');

  const { data, isLoading } = useQuery({
    queryKey: ['enrollments', statusFilter],
    queryFn: () => enrollmentAPI.getAll({ status: statusFilter }),
  });

  const enrollments = data?.data?.data || [];

  const filtered = enrollments.filter((e) => {
    const name = `${e.student?.firstName} ${e.student?.lastName}`.toLowerCase();
    return name.includes(search.toLowerCase());
  });

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Students</h1>
          <p>View and manage student enrollments</p>
        </div>
        <button className="btn btn-primary">+ Enroll Student</button>
      </div>

      {/* Filters */}
      <div style={{ display: 'flex', gap: 10, marginBottom: 16 }}>
        <input
          className="form-input"
          style={{ maxWidth: 280 }}
          placeholder="Search by name..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="form-select"
          style={{ maxWidth: 160 }}
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All statuses</option>
          <option value="active">Active</option>
          <option value="transferred">Transferred</option>
          <option value="promoted">Promoted</option>
          <option value="withdrawn">Withdrawn</option>
        </select>
      </div>

      <div className="card">
        <div className="table-wrapper">
          {isLoading ? (
            <p style={{ color: 'var(--text-muted)', padding: 20, textAlign: 'center' }}>Loading...</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Admission No.</th>
                  <th>Grade</th>
                  <th>Section</th>
                  <th>Roll No.</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((e) => (
                  <tr key={e._id}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <div style={{
                          width: 32, height: 32, borderRadius: '50%',
                          background: 'var(--accent-dim)', display: 'flex',
                          alignItems: 'center', justifyContent: 'center',
                          fontSize: '0.78rem', fontWeight: 600, color: 'var(--accent)',
                          flexShrink: 0,
                        }}>
                          {e.student?.firstName?.[0]}{e.student?.lastName?.[0]}
                        </div>
                        <div>
                          <div style={{ fontWeight: 500, fontSize: '0.88rem' }}>
                            {e.student?.firstName} {e.student?.lastName}
                          </div>
                          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                            {e.student?.email}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td style={{ color: 'var(--text-muted)', fontFamily: 'monospace', fontSize: '0.82rem' }}>
                      {e.admissionNumber || '—'}
                    </td>
                    <td>{e.grade?.name || '—'}</td>
                    <td>
                      <span className="badge badge-blue">{e.section?.name || '—'}</span>
                    </td>
                    <td style={{ color: 'var(--text-muted)' }}>{e.rollNumber || '—'}</td>
                    <td>
                      <span className={`badge ${STATUS_BADGE[e.status] || 'badge-blue'}`}>
                        {e.status}
                      </span>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: 6 }}>
                        <button className="btn btn-ghost btn-sm">View</button>
                        <button className="btn btn-ghost btn-sm">Transfer</button>
                      </div>
                    </td>
                  </tr>
                ))}
                {filtered.length === 0 && !isLoading && (
                  <tr>
                    <td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: 32 }}>
                      No students found. Enroll students to see them here.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
