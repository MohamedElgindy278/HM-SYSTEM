import { BedDouble, DoorOpen, Clock, Activity, AlertTriangle, Droplet } from 'lucide-react';

const TILES = [
  {
    id: 'icu-beds',
    tone: 'tone-danger',
    icon: BedDouble,
    value: '42 / 50',
    label: 'ICU Beds Occupied',
    meter: 84,
  },
  {
    id: 'rooms',
    tone: 'tone-success',
    icon: DoorOpen,
    value: '37',
    label: 'Available Rooms',
    meter: 52,
  },
  {
    id: 'waiting',
    tone: 'tone-warning',
    icon: Clock,
    value: '19',
    label: 'Waiting Patients',
    meter: 38,
  },
  {
    id: 'operation-rooms',
    tone: 'tone-primary',
    icon: Activity,
    value: '5 / 8',
    label: 'Operation Rooms Busy',
    meter: 62,
  },
  {
    id: 'emergency-queue',
    tone: 'tone-danger',
    icon: AlertTriangle,
    value: '7',
    label: 'Emergency Queue',
    pulse: true,
  },
  {
    id: 'blood-bank',
    tone: 'tone-danger',
    icon: Droplet,
    value: 'Adequate',
    label: 'Blood Bank Status',
    meter: 70,
  },
];

function StatusTile({ tile }) {
  const Icon = tile.icon;
  return (
    <div className={`status-tile ${tile.tone}`}>
      <div className="status-icon">
        <Icon size={17} strokeWidth={2} />
      </div>
      <div className="status-body">
        <div className="status-value">{tile.value}</div>
        <div className="status-label">{tile.label}</div>
        {typeof tile.meter === 'number' && (
          <div className="meter">
            <div className="meter-fill" style={{ width: `${tile.meter}%` }} />
          </div>
        )}
      </div>
      {tile.pulse && <span className="pulse" />}
    </div>
  );
}

export default function HospitalStatus() {
  return (
    <>
      <h2 className="section-title">Hospital Status</h2>
      <div className="grid grid-status">
        {TILES.map((tile) => (
          <StatusTile key={tile.id} tile={tile} />
        ))}
      </div>
    </>
  );
}
