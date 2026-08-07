import { BedDouble, DoorOpen, Building2, Stethoscope, Siren, Activity } from 'lucide-react';

import { Card, Loading } from '../../../components/ui';
import { useHospitalStatus } from '../hooks/useDashboard';
import { extractErrorMessage } from '../../../utils/errors';

const AVAILABILITY_TONE = {
  Normal: 'tone-success',
  Busy: 'tone-warning',
  Critical: 'tone-danger',
};

function StatusTile({ tone, Icon, value, label }) {
  return (
    <Card className={`status-tile ${tone}`} hoverable={false}>
      <div className="status-icon">
        <Icon size={20} />
      </div>
      <div className="status-body">
        <div className="status-value">{value}</div>
        <div className="status-label">{label}</div>
      </div>
    </Card>
  );
}

export default function HospitalStatus() {
  const { data: status, isLoading, isError, error } = useHospitalStatus();

  return (
    <>
      <h2 className="section-title">Hospital Status</h2>

      {isLoading && <Loading label="Loading hospital status..." />}
      {isError && <div className="empty-state error">{extractErrorMessage(error)}</div>}

      {!isLoading && !isError && status && (
        <section className="grid grid-status">
          <StatusTile
            tone="tone-primary"
            Icon={BedDouble}
            value={`${status.bed_occupancy?.occupancy_rate ?? 0}%`}
            label="Bed Occupancy"
          />

          <StatusTile
            tone="tone-primary"
            Icon={DoorOpen}
            value={`${status.room_occupancy?.occupied ?? 0} / ${status.room_occupancy?.total ?? 0}`}
            label="Room Occupancy"
          />

          <StatusTile
            tone="tone-primary"
            Icon={Building2}
            value={status.ward_status?.total_wards ?? 0}
            label="Wards"
          />

          <StatusTile
            tone="tone-primary"
            Icon={Stethoscope}
            value={status.clinic_status?.open_clinics ?? 0}
            label="Open Clinics"
          />

          <StatusTile
            tone={
              (status.emergency_queue?.waiting_patients ?? 0) > 0 ? 'tone-danger' : 'tone-success'
            }
            Icon={Siren}
            value={status.emergency_queue?.waiting_patients ?? 0}
            label="Emergency Queue"
          />

          <StatusTile
            tone={AVAILABILITY_TONE[status.hospital_availability?.status] || 'tone-primary'}
            Icon={Activity}
            value={status.hospital_availability?.status ?? '—'}
            label="Hospital Availability"
          />
        </section>
      )}
    </>
  );
}
