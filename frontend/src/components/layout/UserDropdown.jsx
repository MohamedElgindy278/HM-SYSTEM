import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronDown, User, Settings, KeyRound, LogOut } from 'lucide-react';

import { useAuth } from '../../features/auth/context/AuthContext';

import './UserDropdown.css';

export default function UserDropdown() {
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const [open, setOpen] = useState(false);
  const menuRef = useRef(null);
  const triggerRef = useRef(null);

  // إغلاق عند الضغط برا أو Escape
  useEffect(() => {
    if (!open) return;

    function handleClickOutside(event) {
      if (!menuRef.current?.contains(event.target)) {
        setOpen(false);
      }
    }

    function handleKeyDown(event) {
      if (event.key === 'Escape') {
        setOpen(false);
        triggerRef.current?.focus();
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [open]);

  const handleNavigate = (path) => {
    setOpen(false);
    navigate(path);
  };

  const handleLogout = async () => {
    setOpen(false);
    await logout();
  };

  const initials = user?.username?.slice(0, 2).toUpperCase() || '??';
  const rolesLabel = user?.roles?.length ? user.roles.join(', ') : 'Staff';

  return (
    <div className="user-dropdown" ref={menuRef}>
      <button
        ref={triggerRef}
        type="button"
        className="user-dropdown-trigger"
        onClick={() => setOpen((prev) => !prev)}
        aria-expanded={open}
        aria-haspopup="menu"
        aria-label="User menu"
      >
        <div className="user-avatar" aria-hidden="true">
          {initials}
        </div>

        <div className="user-info">
          <h4>{user?.username || 'User'}</h4>
          <span>{rolesLabel}</span>
        </div>

        <ChevronDown
          size={18}
          className={`dropdown-arrow ${open ? 'rotate' : ''}`}
          aria-hidden="true"
        />
      </button>

      {open && (
        <div className="dropdown-menu" role="menu">
          <button
            type="button"
            className="dropdown-item"
            role="menuitem"
            onClick={() => handleNavigate('/profile')}
          >
            <User size={18} aria-hidden="true" />
            My Profile
          </button>

          <button
            type="button"
            className="dropdown-item"
            role="menuitem"
            onClick={() => handleNavigate('/settings')}
          >
            <Settings size={18} aria-hidden="true" />
            Settings
          </button>

          <button
            type="button"
            className="dropdown-item"
            role="menuitem"
            onClick={() => handleNavigate('/change-password')}
          >
            <KeyRound size={18} aria-hidden="true" />
            Change Password
          </button>

          <div className="dropdown-divider" role="separator" />

          <button
            type="button"
            className="dropdown-item logout"
            role="menuitem"
            onClick={handleLogout}
          >
            <LogOut size={18} aria-hidden="true" />
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
