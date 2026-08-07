import { UserPlus, CalendarPlus, BedDouble, ClipboardPlus, Pill, CreditCard } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

import { Button } from '../../../components/ui';

const ACTIONS = [
  { title: 'Add Patient', Icon: UserPlus, path: '/patients/create' },
  { title: 'New Appointment', Icon: CalendarPlus, path: '/appointments/create' },
  { title: 'Manage Beds', Icon: BedDouble, path: '/beds' },
  { title: 'New Encounter', Icon: ClipboardPlus, path: '/encounters/create' },
  { title: 'Prescriptions', Icon: Pill, path: '/prescriptions' },
  { title: 'Payments', Icon: CreditCard, path: '/payments' },
];

export default function QuickActions() {
  const navigate = useNavigate();

  return (
    <>
      <h2 className="section-title">Quick Actions</h2>

      <section className="grid grid-actions">
        {ACTIONS.map(({ title, Icon, path }) => (
          <Button
            key={title}
            variant="outline"
            className="action-card"
            onClick={() => navigate(path)}
            icon={Icon}
          >
            <span className="action-label">{title}</span>
          </Button>
        ))}
      </section>
    </>
  );
}
