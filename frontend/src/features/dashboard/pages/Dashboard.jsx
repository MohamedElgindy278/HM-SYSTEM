import { useNavigate } from 'react-router-dom';

import Header from '../components/Header';
import StatisticsCards from '../components/StatisticsCards';
import QuickActions from '../components/QuickActions';
import HospitalStatus from '../components/HospitalStatus';
import Analytics from '../components/Analytics';
import TodayAppointments from '../components/TodayAppointments';
import RecentActivity from '../components/RecentActivity';

import './Dashboard.css';

export default function Dashboard() {
  const navigate = useNavigate();

  const handleAppointmentAction = (type, appointmentId) => {
    switch (type) {
      case 'view':
        navigate(`/appointments/${appointmentId}`);
        break;
      case 'edit':
        navigate(`/appointments/${appointmentId}/edit`);
        break;
      case 'reschedule':
        navigate(`/appointments/${appointmentId}/reschedule`);
        break;
      default:
        break;
    }
  };

  return (
    <div className="dashboard">
      <Header />
      <StatisticsCards />
      <QuickActions />
      <HospitalStatus />
      <Analytics />
      <TodayAppointments onAction={handleAppointmentAction} />
      <RecentActivity />
    </div>
  );
}
