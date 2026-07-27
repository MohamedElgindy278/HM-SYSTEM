import { UserPlus, Trash2, Pencil, Activity } from 'lucide-react';
import { useRecentActivity } from '../hooks/useDashboard';
import Loading from '../../../components/common/Loading';

const ACTION_LABEL = {
  INSERT: 'created',
  UPDATE: 'updated',
  DELETE: 'deleted',
};

const ACTION_ICON = {
  INSERT: UserPlus,
  UPDATE: Pencil,
  DELETE: Trash2,
};

const ACTION_COLOR = {
  INSERT: '#10b981',
  UPDATE: '#2563eb',
  DELETE: '#ef4444',
};

function formatDate(dateString) {
  return new Date(dateString).toLocaleString([], {
    dateStyle: 'medium',
    timeStyle: 'short',
  });
}

export default function RecentActivity() {
  const { data, loading, error } = useRecentActivity(5);
  const activities = data || [];

  return (
    <>
      <h2 className="section-title">Recent Activity</h2>

      <div className="card">
        {loading && <Loading label="Loading activity..." />}
        {error && <div className="empty-state error">{error}</div>}

        {!loading && !error && (
          <div className="timeline">
            {activities.length === 0 ? (
              <div className="empty-state">No recent activity.</div>
            ) : (
              activities.map((item) => {
                const Icon = ACTION_ICON[item.action] || Activity;
                const color = ACTION_COLOR[item.action] || '#64748b';
                const verb = ACTION_LABEL[item.action] || item.action.toLowerCase();

                return (
                  <div className="t-item" key={item.audit_id}>
                    <div className="t-dot" style={{ background: `${color}20`, color }}>
                      <Icon size={17} />
                    </div>

                    <div className="t-body">
                      <div className="t-text">
                        <strong>{item.changed_by_name ?? 'System'}</strong> {verb}{' '}
                        <strong>{item.table_name}</strong> #{item.record_id}
                      </div>
                      <div className="t-time">{formatDate(item.changed_at)}</div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        )}
      </div>
    </>
  );
}
