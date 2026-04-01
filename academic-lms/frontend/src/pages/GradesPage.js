import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { gradeAPI, sectionAPI } from '../services/api';

const DIVISION_LABELS = {
  primary: 'Primary',
  junior_secondary: 'Junior Secondary',
  senior_secondary: 'Senior Secondary',
  al: 'A/L',
};

const DIVISION_COLORS = {
  primary: 'badge-green',
  junior_secondary: 'badge-blue',
  senior_secondary: 'badge-amber',
  al: 'badge-purple',
};

export default function GradesPage() {
  const qc = useQueryClient();
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ name: '', level: '', division: 'junior_secondary' });

  const { data, isLoading } = useQuery({
    queryKey: ['grades'],
    queryFn: () => gradeAPI.getAll(),
  });

  const { data: sectionsData } = useQuery({
    queryKey: ['sections'],
    queryFn: () => sectionAPI.getAll(),
  });

  const grades = data?.data?.data || [];
  const sections = sectionsData?.data?.data || [];

  const getSectionCount = (gradeId) =>
    sections.filter((s) => s.grade?._id === gradeId || s.grade === gradeId).length;

  const createMutation = useMutation({
    mutationFn: (data) => gradeAPI.create({ ...data, academicYear: '6761a000000000000000000a' }),
    onSuccess: () => {
      qc.invalidateQueries(['grades']);
      toast.success('Grade created!');
      setShowModal(false);
      setForm({ name: '', level: '', division: 'junior_secondary' });
    },
    onError: (err) => toast.error(err.response?.data?.message || 'Failed'),
  });

  const deleteMutation = useMutation({
    mutationFn: gradeAPI.remove,
    onSuccess: () => { qc.invalidateQueries(['grades']); toast.success('Grade deleted'); },
  });

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Grades & Classes</h1>
          <p>Manage school grades, divisions, and sections</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>+ Add Grade</button>
      </div>

      <div className="card">
        <div className="table-wrapper">
          {isLoading ? (
            <p style={{ color: 'var(--text-muted)', padding: 20, textAlign: 'center' }}>Loading...</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Grade</th>
                  <th>Level</th>
                  <th>Division</th>
                  <th>Sections</th>
                  <th>Sectional Head</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {grades.map((g) => (
                  <tr key={g._id}>
                    <td style={{ fontWeight: 600 }}>{g.name}</td>
                    <td style={{ color: 'var(--text-muted)' }}>{g.level}</td>
                    <td>
                      <span className={`badge ${DIVISION_COLORS[g.division] || 'badge-blue'}`}>
                        {DIVISION_LABELS[g.division] || g.division}
                      </span>
                    </td>
                    <td>
                      <span style={{ color: 'var(--accent)', fontWeight: 600 }}>
                        {getSectionCount(g._id)}
                      </span>
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}> sections</span>
                    </td>
                    <td style={{ color: 'var(--text-muted)' }}>
                      {g.sectionalHead
                        ? `${g.sectionalHead.firstName} ${g.sectionalHead.lastName}`
                        : '—'}
                    </td>
                    <td>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => deleteMutation.mutate(g._id)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
                {grades.length === 0 && (
                  <tr>
                    <td colSpan={6} style={{ textAlign: 'center', color: 'var(--text-muted)', padding: 32 }}>
                      No grades found. Run the seed script to add sample data.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Add New Grade</h3>
              <button className="btn btn-ghost btn-sm" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <div className="modal-body">
              <div className="form-group">
                <label className="form-label">Grade Name</label>
                <input
                  className="form-input"
                  placeholder="e.g. Grade 6"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Level (Number)</label>
                <input
                  className="form-input"
                  type="number"
                  placeholder="e.g. 6"
                  value={form.level}
                  onChange={(e) => setForm({ ...form, level: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Division</label>
                <select
                  className="form-select"
                  value={form.division}
                  onChange={(e) => setForm({ ...form, division: e.target.value })}
                >
                  <option value="primary">Primary</option>
                  <option value="junior_secondary">Junior Secondary</option>
                  <option value="senior_secondary">Senior Secondary</option>
                  <option value="al">A/L (Advanced Level)</option>
                </select>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button>
              <button
                className="btn btn-primary"
                disabled={createMutation.isPending}
                onClick={() => createMutation.mutate(form)}
              >
                {createMutation.isPending ? 'Creating...' : 'Create Grade'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
