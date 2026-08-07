import { useState } from 'react';
import { Eye, FilePenLine, CalendarClock } from 'lucide-react';

import { Card, Badge, Button, Loading, Pagination } from '../../../components/ui';
import { useTodayAppointments } from '../hooks/useDashboard';
import { extractErrorMessage } from '../../../utils/errors';

const PAGE_SIZE = 10;

const STATUS_BADGE = {
  Scheduled: 'info',
  Completed: 'success',
  Cancelled: 'danger',
  Pending: 'warning',
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
  const { data, isLoading, isError, error } = useTodayAppointments(page, PAGE_SIZE);

  const appointments = data?.items || [];
  const total = data?.total || 0;

  return (
    <>
      <h2 className="section-title">Today's Appointments</h2>

      <Card className="table-card" hoverable={false}>
        <div className="table-toolbar">
          <span className="table-title">
            {isLoading ? "Today's Appointments" : `${total} appointments today`}
          </span>

          <div className="table-tools">
            <Button variant="outline" size="sm">
              View All
            </Button>
          </div>
        </div>

        <div className="table-wrap">
          {isLoading && <Loading label="Loading appointments..." />}
          {isError && <div className="empty-state error">{extractErrorMessage(error)}</div>}

          {!isLoading && !isError && (
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
                        <Badge tone={STATUS_BADGE[appt.status] || 'info'}>{appt.status}</Badge>
                      </td>

                      <td>
                        <div className="row-actions">
                          <button
                            type="button"
                            className="icon-sm-btn"
                            onClick={() => onAction?.('view', appt.appointment_id)}
                            title="View"
                            aria-label="View appointment"
                          >
                            <Eye size={17} />
                          </button>
                          <button
                            type="button"
                            className="icon-sm-btn"
                            onClick={() => onAction?.('edit', appt.appointment_id)}
                            title="Edit"
                            aria-label="Edit appointment"
                          >
                            <FilePenLine size={17} />
                          </button>
                          <button
                            type="button"
                            className="icon-sm-btn"
                            onClick={() => onAction?.('reschedule', appt.appointment_id)}
                            title="Reschedule"
                            aria-label="Reschedule appointment"
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

        {!isLoading && !isError && total > 0 && (
          <Pagination page={page} pageSize={PAGE_SIZE} total={total} onPageChange={setPage} />
        )}
      </Card>
    </>
  );
}
