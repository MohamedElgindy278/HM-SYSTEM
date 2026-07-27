import { BedDouble, DoorOpen, Building2, Stethoscope, Siren, Activity } from 'lucide-react';
import { useHospitalStatus } from '../hooks/useDashboard';
import Loading from '../../../components/common/Loading';

const AVAILABILITY_TONE = {
  Normal: 'tone-success',
  Busy: 'tone-warning',
  Critical: 'tone-danger',
};

function StatusTile({ tone, Icon, value, label }) {
  return (
    <div className={`status-tile ${tone}`}>
      <div className="status-icon">
        <Icon size={20} />
      </div>
      <div className="status-body">
        <div className="status-value">{value}</div>
        <div className="status-label">{label}</div>
      </div>
    </div>
  );
}

export default function HospitalStatus() {
  const { data: status, loading, error } = useHospitalStatus();

  return (
    <>
      <h2 className="section-title">Hospital Status</h2>

      {loading && <Loading label="Loading hospital status..." />}
      {error && <div className="empty-state error">{error}</div>}

      {!loading && !error && status && (
        <section className="grid grid-status">
          <StatusTile
            tone="tone-primary"
            Icon={BedDouble}
            value={`${status.bed_occupancy.occupancy_rate}%`}
            label="Bed Occupancy"
          />

          <StatusTile
            tone="tone-primary"
            Icon={DoorOpen}
            value={`${status.room_occupancy.occupied} / ${status.room_occupancy.total}`}
            label="Room Occupancy"
          />

          <StatusTile
            tone="tone-primary"
            Icon={Building2}
            value={status.ward_status.total_wards}
            label="Wards"
          />

          <StatusTile
            tone="tone-primary"
            Icon={Stethoscope}
            value={status.clinic_status.open_clinics}
            label="Open Clinics"
          />

          <StatusTile
            tone={status.emergency_queue.waiting_patients > 0 ? 'tone-danger' : 'tone-success'}
            Icon={Siren}
            value={status.emergency_queue.waiting_patients}
            label="Emergency Queue"
          />

          <StatusTile
            tone={AVAILABILITY_TONE[status.hospital_availability.status] || 'tone-primary'}
            Icon={Activity}
            value={status.hospital_availability.status}
            label="Hospital Availability"
          />
        </section>
      )}
    </>
  );
}
