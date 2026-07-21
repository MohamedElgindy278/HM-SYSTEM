import { useEffect, useRef, useState } from 'react';
import { Bell } from 'lucide-react';

import './NotificationDropdown.css';

const MOCK_NOTIFICATIONS = [
  { id: 1, title: 'New appointment booked', time: '5m ago' },
  { id: 2, title: 'Lab result ready for review', time: '1h ago' },
  { id: 3, title: 'Patient record updated', time: '3h ago' },
];

export default function NotificationDropdown() {
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
    <div className="notification-dropdown" ref={menuRef}>
      <button
        className="notification-btn"
        onClick={() => setOpen((prev) => !prev)}
        aria-label="Notifications"
      >
        <Bell size={20} />
        {MOCK_NOTIFICATIONS.length > 0 && (
          <span className="notification-badge">{MOCK_NOTIFICATIONS.length}</span>
        )}
      </button>

      {open && (
        <div className="notification-menu">
          <div className="notification-menu-header">Notifications</div>

          {MOCK_NOTIFICATIONS.length === 0 ? (
            <div className="notification-empty">You're all caught up.</div>
          ) : (
            MOCK_NOTIFICATIONS.map((item) => (
              <div key={item.id} className="notification-item">
                <span className="notification-item-title">{item.title}</span>
                <span className="notification-item-time">{item.time}</span>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
