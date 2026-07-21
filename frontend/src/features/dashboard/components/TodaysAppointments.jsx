import { Search, Filter, MoreHorizontal } from 'lucide-react';

const APPOINTMENTS = [
  {
    id: 'PT-2291',
    patient: 'John Doe',
    patientColor: '#2563EB',
    doctor: 'Dr. Sarah Ahmed',
    doctorColor: '#0EA5E9',
    department: 'Cardiology',
    time: '09:30 AM',
    status: 'Confirmed',
    badge: 'b-success',
  },
  {
    id: 'PT-2288',
    patient: 'Laila Mostafa',
    patientColor: '#10B981',
    doctor: 'Dr. Khaled Hassan',
    doctorColor: '#F59E0B',
    department: 'Pediatrics',
    time: '10:00 AM',
    status: 'Pending',
    badge: 'b-pending',
  },
  {
    id: 'PT-2277',
    patient: 'Ahmed Sami',
    patientColor: '#EF4444',
    doctor: 'Dr. Nour Farid',
    doctorColor: '#06B6D4',
    department: 'Orthopedics',
    time: '11:15 AM',
    status: 'Cancelled',
    badge: 'b-danger',
  },
  {
    id: 'PT-2299',
    patient: 'Rana Youssef',
    patientColor: '#8B5CF6',
    doctor: 'Dr. Mona Saeed',
    doctorColor: '#2563EB',
    department: 'Neurology',
    time: '12:00 PM',
    status: 'Scheduled',
    badge: 'b-info',
  },
  {
    id: 'PT-2265',
    patient: 'Hany Kamal',
    patientColor: '#0EA5E9',
    doctor: 'Dr. Sarah Ahmed',
    doctorColor: '#10B981',
    department: 'Cardiology',
    time: '1:30 PM',
    status: 'Completed',
    badge: 'b-success',
  },
];

function initials(name) {
  return name
    .split(' ')
    .map((p) => p[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();
}

export default function TodaysAppointments({ onRowAction }) {
  return (
    <>
      <h2 className="section-title">Today's Appointments</h2>
      <div className="card table-card">
        <div className="table-toolbar">
          <span className="table-title">{APPOINTMENTS.length} appointments today</span>
          <div className="table-tools">
            <button type="button" className="tbtn">
              <Search size={14} strokeWidth={2} />
              Search
            </button>
            <button type="button" className="tbtn">
              <Filter size={14} strokeWidth={2} />
              Filter
            </button>
          </div>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Department</th>
                <th>Time</th>
                <th>Status</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {APPOINTMENTS.map((row) => (
                <tr key={row.id}>
                  <td>
                    <div className="cell-person">
                      <div className="mini-avatar" style={{ background: row.patientColor }}>
                        {initials(row.patient)}
                      </div>
                      <div>
                        <div className="person-name">{row.patient}</div>
                        <div className="person-sub">#{row.id}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div className="cell-person">
                      <div className="mini-avatar" style={{ background: row.doctorColor }}>
                        {initials(row.doctor)}
                      </div>
                      <div className="person-name">{row.doctor}</div>
                    </div>
                  </td>
                  <td>{row.department}</td>
                  <td>{row.time}</td>
                  <td>
                    <span className={`badge ${row.badge}`}>
                      <span className="bdot" />
                      {row.status}
                    </span>
                  </td>
                  <td className="row-actions">
                    <button
                      type="button"
                      className="icon-sm-btn"
                      onClick={() => onRowAction?.(row.id)}
                    >
                      <MoreHorizontal size={15} strokeWidth={2} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="pagination">
          <span>Showing 1–{APPOINTMENTS.length} of 42</span>
          <div className="page-btns">
            <button type="button" className="page-btn">
              Prev
            </button>
            <button type="button" className="page-btn active">
              1
            </button>
            <button type="button" className="page-btn">
              2
            </button>
            <button type="button" className="page-btn">
              3
            </button>
            <button type="button" className="page-btn">
              Next
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
