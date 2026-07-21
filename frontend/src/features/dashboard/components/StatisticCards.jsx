import {
  Users,
  Stethoscope,
  Calendar,
  BedDouble,
  Wallet,
  AlertTriangle,
  ArrowUp,
  ArrowDown,
} from 'lucide-react';

const STATS = [
  {
    id: 'patients',
    label: 'Total Patients',
    value: '1,284',
    trend: '12%',
    direction: 'up',
    icon: Users,
    gradient: 'g-primary',
    spark: 'M0,22 C10,18 18,24 28,17 C38,10 46,20 56,14 C66,8 76,16 86,9 C92,5 96,7 100,4',
    sparkFill: '#2563EB',
  },
  {
    id: 'doctors',
    label: 'Doctors On Staff',
    value: '96',
    trend: '4%',
    direction: 'up',
    icon: Stethoscope,
    gradient: 'g-secondary',
    spark: 'M0,20 C12,22 20,14 30,16 C42,18 50,10 60,12 C72,14 80,8 90,10 L100,9',
    sparkFill: '#06B6D4',
  },
  {
    id: 'appointments',
    label: 'Appointments Today',
    value: '42',
    trend: '8%',
    direction: 'up',
    icon: Calendar,
    gradient: 'g-info',
    spark: 'M0,24 C15,20 22,26 32,18 C44,10 55,22 66,16 C76,11 86,18 100,6',
    sparkFill: '#0EA5E9',
  },
  {
    id: 'beds',
    label: 'Available Beds',
    value: '128 / 210',
    trend: '2%',
    direction: 'down',
    icon: BedDouble,
    gradient: 'g-success',
    spark: 'M0,10 C10,14 20,8 30,13 C42,18 52,12 62,17 C72,21 84,15 100,20',
    sparkFill: '#10B981',
  },
  {
    id: 'revenue',
    label: 'Revenue (This Month)',
    value: '$48.2K',
    trend: '18%',
    direction: 'up',
    icon: Wallet,
    gradient: 'g-success',
    spark: 'M0,26 C14,24 20,18 32,20 C44,22 52,10 64,12 C76,14 86,4 100,6',
    sparkFill: '#10B981',
  },
  {
    id: 'emergency',
    label: 'Emergency Cases',
    value: '14',
    trend: '3%',
    direction: 'up',
    icon: AlertTriangle,
    gradient: 'g-danger',
    spark: 'M0,18 C10,22 18,10 28,16 C40,22 48,8 58,14 C70,20 80,9 100,15',
    sparkFill: '#EF4444',
    urgent: true,
  },
];

function StatCard({ stat }) {
  const Icon = stat.icon;
  const TrendIcon = stat.direction === 'up' ? ArrowUp : ArrowDown;

  return (
    <div className={`card hoverable stat-card${stat.urgent ? ' urgent' : ''}`}>
      <div className="stat-top">
        <div className={`stat-icon ${stat.gradient}`}>
          <Icon size={20} strokeWidth={2} />
        </div>
        <span className={`trend ${stat.direction}`}>
          <TrendIcon size={11} strokeWidth={3} />
          {stat.trend}
        </span>
      </div>

      <div className="stat-value">{stat.value}</div>
      <div className="stat-label">{stat.label}</div>

      <svg className="spark" viewBox="0 0 100 30" preserveAspectRatio="none">
        <path d={`${stat.spark} L100,30 L0,30 Z`} fill={stat.sparkFill} opacity={0.12} />
        <path
          d={stat.spark}
          fill="none"
          stroke={stat.sparkFill}
          strokeWidth={2}
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
}

export default function StatisticCards() {
  return (
    <div className="grid grid-stats">
      {STATS.map((stat) => (
        <StatCard key={stat.id} stat={stat} />
      ))}
    </div>
  );
}
