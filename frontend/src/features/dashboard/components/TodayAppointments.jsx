import { useState } from 'react';
import { Eye, FilePenLine, CalendarClock } from 'lucide-react';
import { useTodayAppointments } from '../hooks/useDashboard';
import Pagination from '../../../components/common/Pagination';
import Loading from '../../../components/common/Loading';

const PAGE_SIZE = 10;

const STATUS_BADGE = {
  Scheduled: 'b-info',
  Completed: 'b-success',
  Cancelled: 'b-danger',
};

function initials(name = '') {
  return name
    .split(' ')
    .filter(Boolean)
    .map((p) => p[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();
}

function formatTime(dateString) {
  if (!dateString) return '';
  return new Date(dateString).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
}

export default function TodayAppointments({ onAction }) {
  const [page, setPage] = useState(1);
  const { data, loading, error } = useTodayAppointments(page, PAGE_SIZE);

  const appointments = data?.items || [];
  const total = data?.total || 0;

  return (
    <>
      <h2 className="section-title">Today's Appointments</h2>

      <div className="card table-card">
        <div className="table-toolbar">
          <span className="table-title">
            {loading ? "Today's Appointments" : `${total} appointments today`}
          </span>
        </div>

        <div className="table-wrap">
          {loading && <Loading label="Loading appointments..." />}
          {error && <div className="empty-state error">{error}</div>}

          {!loading && !error && (
            <table>
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Patient</th>
                  <th>Doctor</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {appointments.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="empty-state">
                      No appointments today.
                    </td>
                  </tr>
                ) : (
                  appointments.map((appt) => (
                    <tr key={appt.appointment_id}>
                      <td>{formatTime(appt.appointment_date)}</td>

                      <td>
                        <div className="cell-person">
                          <div className="mini-avatar">{initials(appt.patient_name)}</div>
                          <div>
                            <div className="person-name">{appt.patient_name}</div>
                            <div className="person-sub">#{appt.patient_id}</div>
                          </div>
                        </div>
                      </td>

                      <td>{appt.doctor_name}</td>

                      <td>
                        <span className={`badge ${STATUS_BADGE[appt.status] || 'b-info'}`}>
                          <span className="bdot" />
                          {appt.status}
                        </span>
                      </td>

                      <td>
                        <div className="row-actions">
                          <button
                            className="icon-sm-btn"
                            onClick={() => onAction?.('view', appt.appointment_id)}
                            title="View"
                          >
                            <Eye size={17} />
                          </button>
                          <button
                            className="icon-sm-btn"
                            onClick={() => onAction?.('edit', appt.appointment_id)}
                            title="Edit"
                          >
                            <FilePenLine size={17} />
                          </button>
                          <button
                            className="icon-sm-btn"
                            onClick={() => onAction?.('reschedule', appt.appointment_id)}
                            title="Reschedule"
                          >
                            <CalendarClock size={17} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </div>

        {!loading && !error && total > 0 && (
          <Pagination page={page} pageSize={PAGE_SIZE} total={total} onPageChange={setPage} />
        )}
      </div>
    </>
  );
}
