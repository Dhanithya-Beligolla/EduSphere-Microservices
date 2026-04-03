import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { gradeAPI, enrollmentAPI, subjectAPI, teacherAssignmentAPI } from '../services/api';

const CHART_DATA = [
  { grade: 'G6', students: 120 },
  { grade: 'G7', students: 115 },
  { grade: 'G8', students: 108 },
  { grade: 'G9', students: 98 },
  { grade: 'G10', students: 90 },
  { grade: 'G11', students: 85 },
  { grade: 'G12', students: 60 },
  { grade: 'G13', students: 54 },
];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div className="card" style={{ padding: '10px 14px', fontSize: '0.8rem' }}>
        <div style={{ color: 'var(--text-muted)', marginBottom: 2 }}>{label}</div>
        <div style={{ color: 'var(--accent)', fontWeight: 600 }}>{payload[0].value} students</div>
      </div>
    );
  }
  return null;
};

export default function DashboardPage() {
  const { data: gradesData } = useQuery({ queryKey: ['grades'], queryFn: () => gradeAPI.getAll() });
  const { data: subjectsData } = useQuery({ queryKey: ['subjects'], queryFn: () => subjectAPI.getAll() });
  const { data: enrollmentsData } = useQuery({
    queryKey: ['enrollments'],
    queryFn: () => enrollmentAPI.getAll({ status: 'active' }),
  });

  const grades = gradesData?.data?.data || [];
  const subjects = subjectsData?.data?.data || [];
  const enrollments = enrollmentsData?.data?.data || [];

  const stats = [
    { label: 'Total Grades', value: grades.length || 8, icon: '🏫', color: 'blue' },
    { label: 'Active Students', value: enrollments.length || 730, icon: '👨‍🎓', color: 'green' },
    { label: 'Subjects Offered', value: subjects.length || 10, icon: '📚', color: 'amber' },
    { label: 'Teachers', value: 42, icon: '👩‍🏫', color: 'purple' },
  ];

  return (
    <div>
      {/* Stats */}
      <div className="stat-grid">
        {stats.map((s) => (
          <div key={s.label} className="stat-card">
            <div className={`stat-icon ${s.color}`}>{s.icon}</div>
            <div className="stat-info">
              <div className="value">{s.value}</div>
              <div className="label">{s.label}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Chart + Recent Events */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: 16 }}>
        <div className="card">
          <h3 style={{ marginBottom: 20, fontSize: '0.95rem' }}>Student Distribution by Grade</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={CHART_DATA} barSize={28}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis
                dataKey="grade"
                tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
                axisLine={false} tickLine={false}
              />
              <YAxis
                tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
                axisLine={false} tickLine={false}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(79,142,247,0.04)' }} />
              <Bar dataKey="students" fill="var(--accent)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 style={{ marginBottom: 16, fontSize: '0.95rem' }}>Recent Events</h3>
          {[
            { icon: '📋', text: 'Grade 10A class list updated', time: '2m ago', color: 'var(--accent)' },
            { icon: '👤', text: 'Kavya J. enrolled in Grade 9B', time: '14m ago', color: 'var(--green)' },
            { icon: '📅', text: 'Timetable published — Grade 12', time: '1h ago', color: 'var(--purple)' },
            { icon: '🔄', text: 'Student transferred: 8A → 8B', time: '3h ago', color: 'var(--amber)' },
            { icon: '➕', text: 'New subject added: ICT', time: '1d ago', color: 'var(--accent)' },
          ].map((ev, i) => (
            <div
              key={i}
              style={{
                display: 'flex', gap: 10, alignItems: 'flex-start',
                padding: '10px 0',
                borderBottom: i < 4 ? '1px solid var(--border)' : 'none',
              }}
            >
              <div style={{
                width: 30, height: 30, borderRadius: 8,
                background: 'var(--bg)', display: 'flex', alignItems: 'center',
                justifyContent: 'center', fontSize: '0.9rem', flexShrink: 0,
              }}>
                {ev.icon}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '0.8rem' }}>{ev.text}</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 2 }}>{ev.time}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
