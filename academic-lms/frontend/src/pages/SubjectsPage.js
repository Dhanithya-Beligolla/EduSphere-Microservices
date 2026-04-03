import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { subjectAPI } from '../services/api';

const TYPE_BADGE = { core: 'badge-green', optional: 'badge-amber', extra_curricular: 'badge-purple' };

export default function SubjectsPage() {
  const qc = useQueryClient();
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({
    name: '', code: '', type: 'core',
    periodsPerWeek: 5, medium: 'sinhala', applicableGrades: '',
  });

  const { data, isLoading } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => subjectAPI.getAll(),
  });

  const subjects = data?.data?.data || [];

  const createMutation = useMutation({
    mutationFn: (d) => subjectAPI.create({
      ...d,
      applicableGrades: d.applicableGrades.split(',').map((n) => parseInt(n.trim())).filter(Boolean),
    }),
    onSuccess: () => {
      qc.invalidateQueries(['subjects']);
      toast.success('Subject created!');
      setShowModal(false);
      setForm({ name: '', code: '', type: 'core', periodsPerWeek: 5, medium: 'sinhala', applicableGrades: '' });
    },
    onError: (err) => toast.error(err.response?.data?.message || 'Failed'),
  });

  const deleteMutation = useMutation({
    mutationFn: subjectAPI.remove,
    onSuccess: () => { qc.invalidateQueries(['subjects']); toast.success('Subject deleted'); },
  });

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Subjects</h1>
          <p>Manage the school subject catalog</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Add Subject</button>
      </div>

      <div className="card">
        <div className="table-wrapper">
          {isLoading ? (
            <p style={{ color: 'var(--text-muted)', padding: 20, textAlign: 'center' }}>Loading...</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Subject</th>
                  <th>Code</th>
                  <th>Type</th>
                  <th>Medium</th>
                  <th>Periods/Week</th>
                  <th>Applicable Grades</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {subjects.map((s) => (
                  <tr key={s._id}>
                    <td style={{ fontWeight: 500 }}>{s.name}</td>
                    <td>
                      <span style={{
                        fontFamily: 'monospace', fontSize: '0.8rem',
                        background: 'var(--bg)', padding: '2px 8px',
                        borderRadius: 4, color: 'var(--accent)',
                      }}>
                        {s.code}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${TYPE_BADGE[s.type] || 'badge-blue'}`}>{s.type}</span>
                    </td>
                    <td style={{ textTransform: 'capitalize', color: 'var(--text-muted)' }}>
                      {s.medium}
                    </td>
                    <td style={{ color: 'var(--accent)', fontWeight: 600 }}>{s.periodsPerWeek}</td>
                    <td>
                      <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                        {(s.applicableGrades || []).map((g) => (
                          <span key={g} className="badge badge-blue" style={{ fontSize: '0.66rem' }}>
                            G{g}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td>
                      <button className="btn btn-danger btn-sm" onClick={() => deleteMutation.mutate(s._id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
                {subjects.length === 0 && (
                  <tr>
                    <td colSpan={7} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: 32 }}>
                      No subjects. Run the seed script or add one above.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Add Subject</h3>
              <button className="btn btn-ghost btn-sm" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <div className="modal-body">
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <div className="form-group">
                  <label className="form-label">Subject Name</label>
                  <input className="form-input" placeholder="Mathematics" value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })} />
                </div>
                <div className="form-group">
                  <label className="form-label">Code</label>
                  <input className="form-input" placeholder="MATH" value={form.code}
                    onChange={(e) => setForm({ ...form, code: e.target.value.toUpperCase() })} />
                </div>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                <div className="form-group">
                  <label className="form-label">Type</label>
                  <select className="form-select" value={form.type}
                    onChange={(e) => setForm({ ...form, type: e.target.value })}>
                    <option value="core">Core</option>
                    <option value="optional">Optional</option>
                    <option value="extra_curricular">Extra Curricular</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Medium</label>
                  <select className="form-select" value={form.medium}
                    onChange={(e) => setForm({ ...form, medium: e.target.value })}>
                    <option value="sinhala">Sinhala</option>
                    <option value="tamil">Tamil</option>
                    <option value="english">English</option>
                  </select>
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Periods per Week</label>
                <input className="form-input" type="number" value={form.periodsPerWeek}
                  onChange={(e) => setForm({ ...form, periodsPerWeek: Number(e.target.value) })} />
              </div>
              <div className="form-group">
                <label className="form-label">Applicable Grades (comma-separated)</label>
                <input className="form-input" placeholder="6, 7, 8, 9, 10" value={form.applicableGrades}
                  onChange={(e) => setForm({ ...form, applicableGrades: e.target.value })} />
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="btn btn-primary" disabled={createMutation.isPending}
                onClick={() => createMutation.mutate(form)}>
                {createMutation.isPending ? 'Creating...' : 'Create Subject'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
