import { NavLink, Outlet, useLocation } from 'react-router-dom';

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', icon: '⊞', section: 'Overview' },
  { to: '/grades', label: 'Grades & Classes', icon: '🏫', section: 'Academic' },
  { to: '/subjects', label: 'Subjects', icon: '📚', section: 'Academic' },
  { to: '/students', label: 'Students', icon: '👨‍🎓', section: 'People' },
  { to: '/teachers', label: 'Teachers', icon: '👩‍🏫', section: 'People' },
  { to: '/timetable', label: 'Timetable', icon: '🗓', section: 'Schedule' },
];

const PAGE_TITLES = {
  '/': 'Dashboard',
  '/grades': 'Grades & Classes',
  '/subjects': 'Subjects',
  '/students': 'Students',
  '/teachers': 'Teachers',
  '/timetable': 'Timetable',
};

export default function Layout() {
  const location = useLocation();
  const title = PAGE_TITLES[location.pathname] || 'Academic LMS';
  const sections = [...new Set(NAV_ITEMS.map((i) => i.section))];

  return (
    <div className="app-layout">
      {/* ── SIDEBAR ── */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <h2>🎓 Academic LMS</h2>
          <span>Sri Lankan School System</span>
        </div>

        <nav className="sidebar-nav">
          {sections.map((section) => (
            <div key={section}>
              <div className="nav-section-label">{section}</div>
              {NAV_ITEMS.filter((i) => i.section === section).map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.to === '/'}
                  className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
                >
                  <span className="nav-icon">{item.icon}</span>
                  {item.label}
                </NavLink>
              ))}
            </div>
          ))}
        </nav>
      </aside>

      {/* ── MAIN ── */}
      <div className="main-content">
        <header className="topbar">
          <div className="topbar-title">{title}</div>
          <div className="topbar-right">
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Academic Year 2024
            </span>
          </div>
        </header>
        <div className="page-content">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
