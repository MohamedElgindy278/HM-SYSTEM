import { useEffect, useRef, useState } from 'react';
import { Bell } from 'lucide-react';

import './NotificationDropdown.css';

// TODO: استبدل بـ API حقيقي لما يبقى endpoint /notifications جاهز
const MOCK_NOTIFICATIONS = [
  {
    id: 1,
    title: 'New appointment booked',
    description: 'John Doe scheduled for 10:30 AM',
    time: '5m ago',
    unread: true,
  },
  {
    id: 2,
    title: 'Lab result ready',
    description: 'Blood panel for patient #2288 is ready',
    time: '1h ago',
    unread: true,
  },
  {
    id: 3,
    title: 'Patient record updated',
    description: 'Rana Youssef profile was modified',
    time: '3h ago',
    unread: false,
  },
];

export default function NotificationDropdown() {
  const [open, setOpen] = useState(false);
  const [notifications, setNotifications] = useState(MOCK_NOTIFICATIONS);
  const menuRef = useRef(null);
  const triggerRef = useRef(null);

  const unreadCount = notifications.filter((n) => n.unread).length;

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

  const markAllRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, unread: false })));
  };

  const markAsRead = (id) => {
    setNotifications((prev) => prev.map((n) => (n.id === id ? { ...n, unread: false } : n)));
  };

  return (
    <div className="notification-dropdown" ref={menuRef}>
      <button
        ref={triggerRef}
        type="button"
        className="notification-btn"
        onClick={() => setOpen((prev) => !prev)}
        aria-expanded={open}
        aria-haspopup="true"
        aria-label={`Notifications${unreadCount > 0 ? `, ${unreadCount} unread` : ''}`}
      >
        <Bell size={20} aria-hidden="true" />
        {unreadCount > 0 && (
          <span className="notification-badge" aria-hidden="true">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="notification-menu" role="menu">
          <div className="notification-menu-header">
            <span>Notifications</span>
            {unreadCount > 0 && (
              <button type="button" className="mark-all-read" onClick={markAllRead}>
                Mark all as read
              </button>
            )}
          </div>

          {notifications.length === 0 ? (
            <div className="notification-empty">
              <span className="empty-icon" aria-hidden="true">
                🔔
              </span>
              You're all caught up.
            </div>
          ) : (
            notifications.map((item) => (
              <button
                key={item.id}
                type="button"
                className={`notification-item ${item.unread ? 'unread' : ''}`}
                role="menuitem"
                onClick={() => markAsRead(item.id)}
              >
                <span className="notification-item-title">{item.title}</span>
                {item.description && (
                  <span className="notification-item-description">{item.description}</span>
                )}
                <span className="notification-item-time">{item.time}</span>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
}
