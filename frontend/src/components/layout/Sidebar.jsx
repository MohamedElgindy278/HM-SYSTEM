import { NavLink } from 'react-router-dom';
import { ChevronLeft, ChevronRight, X, LogOut } from 'lucide-react';
import { useState } from 'react';

import { useAuth } from '../../features/auth/context/AuthContext';
import { getVisibleSidebarItems } from './sidebarData';

import './Sidebar.css';

export default function Sidebar({ sidebarOpen, setSidebarOpen }) {
  const [collapsed, setCollapsed] = useState(false);
  const { logout, user } = useAuth();
  const permissions = user?.permissions || [];

  const visibleSections = getVisibleSidebarItems(permissions);
  return (
    <>
      <div
        className={`sidebar-overlay ${sidebarOpen ? 'show' : ''}`}
        onClick={() => setSidebarOpen(false)}
      />

      <aside
        className={`sidebar ${collapsed ? 'collapsed' : ''} ${sidebarOpen ? 'mobile-open' : ''}`}
      >
        {/* ================= Logo ================= */}

        <div className="sidebar-header">
          <div className="sidebar-logo">
            <div className="logo-icon">
              <span>M</span>
            </div>

            <div className="logo-text">
              <h2>MedCore</h2>
              <span>Hospital System</span>
            </div>
          </div>

          <div className="close-btn-div">
            <button
              className="collapse-btn"
              onClick={() => setCollapsed((prev) => !prev)}
              aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
              {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
            </button>

            <button
              className="mobile-close-btn"
              onClick={() => setSidebarOpen(false)}
              aria-label="Close menu"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        {/* ================= Navigation ================= */}

        <nav className="sidebar-nav">
          {visibleSections.map((group) => (
            <div key={group.section} className="sidebar-section">
              <span className="section-title">{group.section}</span>

              {group.items.map((item) => {
                const Icon = item.icon;

                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
                    onClick={() => setSidebarOpen(false)}
                  >
                    <Icon size={20} className="sidebar-icon" />
                    <span className="sidebar-link-label">{item.title}</span>
                  </NavLink>
                );
              })}
            </div>
          ))}
        </nav>

        {/* ================= Footer ================= */}

        <div className="sidebar-footer">
          <button className="logout-btn" onClick={logout}>
            <LogOut size={19} />
            <span className="sidebar-link-label">Logout</span>
          </button>
        </div>
      </aside>
    </>
  );
}
