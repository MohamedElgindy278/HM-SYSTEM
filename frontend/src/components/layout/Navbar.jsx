import { Menu, Search } from 'lucide-react';
import { useLocation } from 'react-router-dom';

import { Input } from '../ui';
import UserDropdown from './UserDropdown.jsx';
import NotificationDropdown from './NotificationDropdown.jsx';
import { getPageTitle } from './sidebarData';

import './Navbar.css';

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
          aria-expanded={sidebarOpen}
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
        <Input
          icon={Search}
          type="text"
          placeholder="Search patients, doctors, appointments..."
          className="navbar-search-input"
          aria-label="Search"
        />
      </div>

      {/* ================= Right ================= */}

      <div className="navbar-right">
        <NotificationDropdown />
        <UserDropdown />
      </div>
    </header>
  );
}
