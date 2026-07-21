import { useEffect, useRef, useState } from 'react';
import { ChevronDown, User, Settings, KeyRound, LogOut } from 'lucide-react';

import { useAuth } from '../../features/auth/context/AuthContext';

import './UserDropdown.css';

export default function UserDropdown() {
  const { logout, user } = useAuth();

  const [open, setOpen] = useState(false);

  const menuRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (!menuRef.current?.contains(event.target)) {
        setOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);

    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="user-dropdown" ref={menuRef}>
      <button className="user-dropdown-trigger" onClick={() => setOpen((prev) => !prev)}>
        <div className="user-avatar">{user?.data?.username?.slice(0, 2).toUpperCase()}</div>

        <div className="user-info">
          <h4>{user?.data?.username}</h4>
          <span>{user?.data?.roles?.join(', ')}</span>
        </div>

        <ChevronDown size={18} className={`dropdown-arrow ${open ? 'rotate' : ''}`} />
      </button>

      {open && (
        <div className="dropdown-menu">
          <button className="dropdown-item">
            <User size={18} />
            My Profile
          </button>

          <button className="dropdown-item">
            <Settings size={18} />
            Settings
          </button>

          <button className="dropdown-item">
            <KeyRound size={18} />
            Change Password
          </button>

          <div className="dropdown-divider" />

          <button className="dropdown-item logout" onClick={logout}>
            <LogOut size={18} />
            Logout
          </button>
        </div>
      )}
    </div>
  );
}
