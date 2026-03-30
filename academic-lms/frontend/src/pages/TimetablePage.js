import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import toast from 'react-hot-toast';
import { timetableAPI, sectionAPI, subjectAPI } from '../services/api';

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
const PERIODS = [
  { num: 1, start: '07:30', end: '08:15' },
  { num: 2, start: '08:15', end: '09:00' },
  { num: 3, start: '09:00', end: '09:45' },
  { num: 4, start: '10:05', end: '10:50' }, // after break
  { num: 5, start: '10:50', end: '11:35' },
  { num: 6, start: '11:35', end: '12:20' },
  { num: 7, start: '13:00', end: '13:45' }, // after lunch
  { num: 8, start: '13:45', end: '14:30' },
];

export default function TimetablePage() {
  const qc = useQueryClient();
  const [selectedSection, setSelectedSection] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [selected, setSelected] = useState({ day: null, period: null });
  const [slotForm, setSlotForm] = useState({ subject: '', teacher: '' });

  const { data: sectionsData } = useQuery({
    queryKey: ['sections'],
    queryFn: () => sectionAPI.getAll(),
  });

  const { data: subjectsData } = useQuery({
    queryKey: ['subjects'],
    queryFn: () => subjectAPI.getAll(),
  });

  const { data: timetableData } = useQuery({
    queryKey: ['timetable', selectedSection],
    queryFn: () => timetableAPI.get({ section: selectedSection }),
    enabled: !!selectedSection,
  });

  const sections = sectionsData?.data?.data || [];
  const subjects = subjectsData?.data?.data || [];
  const slots = timetableData?.data?.data || [];

  const getSlot = (dayIndex, periodNum) =>
    slots.find((s) => s.dayOfWeek === dayIndex + 1 && s.periodNumber === periodNum);

  const publishMutation = useMutation({
    mutationFn: () =>
      timetableAPI.publish({ sectionId: selectedSection, academicYearId: '' }),
    onSuccess: () => toast.success('Timetable published! 📅'),
    onError: () => toast.error('Publish failed'),
  });

  const createSlotMutation = useMutation({
    mutationFn: (data) => timetableAPI.createSlot(data),
    onSuccess: () => {
      qc.invalidateQueries(['timetable', selectedSection]);
      toast.success('Slot added!');
      setShowModal(false);
    },
    onError: (err) => toast.error(err.response?.data?.message || 'Conflict detected'),
  });

  const deleteSlotMutation = useMutation({
    mutationFn: (id) => timetableAPI.remove(id),
    onSuccess: () => {
      qc.invalidateQueries(['timetable', selectedSection]);
      toast.success('Slot removed');
    },
  });

  const handleCellClick = (dayIdx, period) => {
    if (!selectedSection) return toast.error('Select a section first');
    const existing = getSlot(dayIdx, period.num);
    if (existing) return; // already filled
    setSelected({ day: dayIdx + 1, period });
    setSlotForm({ subject: '', teacher: '' });
    setShowModal(true);
  };

  const handleCreateSlot = () => {
    const period = selected.period;
    createSlotMutation.mutate({
      section: selectedSection,
      subject: slotForm.subject,
      teacher: slotForm.teacher || '6761a000000000000000000b', // fallback placeholder
      academicYear: '6761a000000000000000000a',
      dayOfWeek: selected.day,
      periodNumber: period.num,
      startTime: period.start,
      endTime: period.end,
    });
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Timetable</h1>
          <p>View and manage weekly class schedules</p>
        </div>
        <div style={{ display: 'flex', gap: 10 }}>
          {selectedSection && (
            <button
              className="btn btn-ghost"
              onClick={() => publishMutation.mutate()}
              disabled={publishMutation.isPending}
            >
              📅 Publish Timetable
            </button>
          )}
        </div>
      </div>

      {/* Section Selector */}
      <div style={{ marginBottom: 20 }}>
        <select
          className="form-select"
          style={{ maxWidth: 240 }}
          value={selectedSection}
          onChange={(e) => setSelectedSection(e.target.value)}
        >
          <option value="">— Select a class section —</option>
          {sections.map((s) => (
            <option key={s._id} value={s._id}>
              {s.grade?.name} — Section {s.name}
            </option>
          ))}
        </select>
      </div>

      {/* Timetable Grid */}
      <div className="card" style={{ overflowX: 'auto' }}>
        {!selectedSection ? (
          <div style={{ textAlign: 'center', padding: 48, color: 'var(--text-muted)' }}>
            <div style={{ fontSize: '2rem', marginBottom: 12 }}>🗓</div>
            <div>Select a class section to view its timetable</div>
          </div>
        ) : (
          <div className="timetable-grid" style={{ minWidth: 700 }}>
            {/* Header row */}
            <div className="tt-header" />
            {DAYS.map((d) => (
              <div key={d} className="tt-header">{d}</div>
            ))}

            {/* Period rows */}
            {PERIODS.map((period) => (
              <>
                <div key={`label-${period.num}`} className="tt-period-label">
                  <span style={{ fontWeight: 700, color: 'var(--accent)' }}>P{period.num}</span>
                  <span style={{ fontSize: '0.6rem', marginTop: 2 }}>{period.start}</span>
                  <span style={{ fontSize: '0.6rem' }}>{period.end}</span>
                </div>
                {DAYS.map((_, dayIdx) => {
                  const slot = getSlot(dayIdx, period.num);
                  return (
                    <div
                      key={`cell-${period.num}-${dayIdx}`}
                      className={`tt-cell ${slot ? 'filled' : ''}`}
                      onClick={() => handleCellClick(dayIdx, period)}
                    >
                      {slot ? (
                        <div>
                          <div className="subject-name">
                            {slot.subject?.name || slot.subject?.code || 'Subject'}
                          </div>
                          <div className="teacher-name">
                            {slot.teacher?.firstName} {slot.teacher?.lastName}
                          </div>
                          <button
                            className="btn btn-danger btn-sm"
                            style={{ marginTop: 4, fontSize: '0.62rem', padding: '2px 6px' }}
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteSlotMutation.mutate(slot._id);
                            }}
                          >
                            ✕
                          </button>
                        </div>
                      ) : (
                        <div style={{
                          height: '100%', display: 'flex', alignItems: 'center',
                          justifyContent: 'center', color: 'var(--text-muted)',
                          fontSize: '1.1rem', opacity: 0.3,
                        }}>
                          +
                        </div>
                      )}
                    </div>
                  );
                })}
              </>
            ))}
          </div>
        )}
      </div>

      {/* Add Slot Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                Add Slot — {DAYS[selected.day - 1]}, Period {selected.period?.num}
              </h3>
              <button className="btn btn-ghost btn-sm" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <div className="modal-body">
              <div style={{
                background: 'var(--bg)',
                borderRadius: 8, padding: '8px 14px',
                marginBottom: 16, fontSize: '0.8rem', color: 'var(--text-muted)',
              }}>
                🕐 {selected.period?.start} – {selected.period?.end}
              </div>
              <div className="form-group">
                <label className="form-label">Subject</label>
                <select
                  className="form-select"
                  value={slotForm.subject}
                  onChange={(e) => setSlotForm({ ...slotForm, subject: e.target.value })}
                >
                  <option value="">— Select subject —</option>
                  {subjects.map((s) => (
                    <option key={s._id} value={s._id}>{s.name} ({s.code})</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Teacher ID (optional)</label>
                <input
                  className="form-input"
                  placeholder="Paste teacher ObjectId"
                  value={slotForm.teacher}
                  onChange={(e) => setSlotForm({ ...slotForm, teacher: e.target.value })}
                />
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 4 }}>
                  Connect a teacher list to pick from dropdown
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-ghost" onClick={() => setShowModal(false)}>Cancel</button>
              <button
                className="btn btn-primary"
                disabled={!slotForm.subject || createSlotMutation.isPending}
                onClick={handleCreateSlot}
              >
                {createSlotMutation.isPending ? 'Adding...' : 'Add Slot'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
