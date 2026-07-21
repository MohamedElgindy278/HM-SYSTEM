import Header from '../components/Header';
import StatisticCards from '../components/StatisticCards';
import QuickActions from '../components/QuickActions';
import HospitalStatus from '../components/HospitalStatus';
import Analytics from '../components/Analytics';
import TodaysAppointments from '../components/TodaysAppointments';
import RecentActivity from '../components/RecentActivity';

import { useAuth } from '../../auth/context/AuthContext';

import './dashboard.css';

export default function Dashboard() {
  const { user } = useAuth();

  console.log(user);
  return (
    <div className="dashboard">
      <Header name={user?.data?.username} />

      <StatisticCards />

      <QuickActions onAction={(id) => console.log('quick action:', id)} />

      <HospitalStatus />

      <Analytics />

      <TodaysAppointments onRowAction={(id) => console.log('row action:', id)} />

      <RecentActivity />
    </div>
  );
}
