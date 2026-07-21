import {
  UserPlus,
  CalendarPlus,
  Stethoscope,
  FilePlus2,
  FileBarChart2,
  Receipt,
} from 'lucide-react';

const ACTIONS = [
  { id: 'add-patient', label: 'Add Patient', icon: UserPlus },
  { id: 'book-appointment', label: 'Book Appointment', icon: CalendarPlus },
  { id: 'register-doctor', label: 'Register Doctor', icon: Stethoscope },
  { id: 'create-prescription', label: 'Create Prescription', icon: FilePlus2 },
  { id: 'generate-report', label: 'Generate Report', icon: FileBarChart2 },
  { id: 'create-invoice', label: 'Create Invoice', icon: Receipt },
];

export default function QuickActions({ onAction }) {
  return (
    <>
      <h2 className="section-title">Quick Actions</h2>
      <div className="grid grid-actions">
        {ACTIONS.map(({ id, label, icon: Icon }) => (
          <button key={id} type="button" className="action-card" onClick={() => onAction?.(id)}>
            <div className="action-icon">
              <Icon size={19} strokeWidth={2} />
            </div>
            <span className="action-label">{label}</span>
          </button>
        ))}
      </div>
    </>
  );
}
