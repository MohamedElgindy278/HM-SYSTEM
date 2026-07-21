import { Menu, Search } from 'lucide-react';

import './Navbar.css';
import UserDropdown from './UserDropdown.jsx';
import NotificationDropdown from './NotificationDropdown.jsx';
import { useLocation } from 'react-router-dom';
import { getPageTitle } from './sidebarData';

export default function Navbar({ sidebarOpen, setSidebarOpen }) {
  const location = useLocation();

  const currentPage = getPageTitle(location.pathname);
  return (
    <header className="navbar">
      {/* ================= Left ================= */}

      <div className="navbar-left">
        <button
          className="menu-btn"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          aria-label="Toggle menu"
        >
          <Menu size={22} />
        </button>

        <div className="breadcrumb">
          <span className="breadcrumb-parent">Dashboard</span>
          <span className="breadcrumb-separator">/</span>
          <span className="breadcrumb-current">{currentPage}</span>
        </div>
      </div>

      {/* ================= Center ================= */}

      <div className="navbar-center">
        <div className="search-box">
          <Search size={18} className="search-icon" />
          <input type="text" placeholder="Search patients, doctors, appointments..." />
        </div>
      </div>

      {/* ================= Right ================= */}

      <div className="navbar-right">
        <NotificationDropdown />
        <UserDropdown />
      </div>
    </header>
  );
}
