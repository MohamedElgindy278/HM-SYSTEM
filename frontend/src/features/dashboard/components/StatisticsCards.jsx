import {
  Users,
  UserRound,
  CalendarDays,
  BedDouble,
  DollarSign,
  TriangleAlert,
  TrendingUp,
  TrendingDown,
} from 'lucide-react';

import { Card, Loading } from '../../../components/ui';
import { useDashboardStats } from '../hooks/useDashboard';
import { extractErrorMessage } from '../../../utils/errors';

const CARD_META = [
  { key: 'total_patients', title: 'Total Patients', Icon: Users, gradient: 'g-primary' },
  { key: 'total_doctors', title: 'Doctors', Icon: UserRound, gradient: 'g-secondary' },
  {
    key: 'appointments_today',
    title: 'Appointments Today',
    Icon: CalendarDays,
    gradient: 'g-success',
  },
  { key: 'available_beds', title: 'Available Beds', Icon: BedDouble, gradient: 'g-warning' },
  { key: 'today_revenue', title: "Today's Revenue", Icon: DollarSign, gradient: 'g-info' },
  { key: 'emergency_cases', title: 'Emergency Cases', Icon: TriangleAlert, gradient: 'g-danger' },
];

function formatValue(key, value) {
  if (key === 'today_revenue') {
    return `$${Number(value).toLocaleString()}`;
  }
  return value;
}

function StatCard({ title, Icon, gradient, item, valueKey }) {
  const hasTrend = item?.trend !== null && item?.trend !== undefined;
  const positive = hasTrend && item.trend >= 0;
  const TrendIcon = positive ? TrendingUp : TrendingDown;

  return (
    <Card hoverable className="stat-card">
      <div className="stat-card-top">
        <div className={`stat-icon ${gradient}`}>
          <Icon size={22} />
        </div>

        {hasTrend && (
          <div className={`trend ${positive ? 'up' : 'down'}`}>
            <TrendIcon size={14} />
            {Math.abs(item.trend)}%
          </div>
        )}
      </div>

      <div className="stat-card-body">
        <span className="stat-value">{formatValue(valueKey, item?.value)}</span>
        <span className="stat-label">{title}</span>
      </div>
    </Card>
  );
}

export default function StatisticsCards() {
  const { data: stats, isLoading, isError, error } = useDashboardStats();

  return (
    <>
      <h2 className="section-title">Overview</h2>

      {isLoading && (
        <section className="statistics-cards">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="skeleton skeleton-stat" />
          ))}
        </section>
      )}
      {isError && <div className="empty-state error">{extractErrorMessage(error)}</div>}

      {!isLoading && !isError && stats && (
        <section className="statistics-cards">
          {CARD_META.map(({ key, title, Icon, gradient }) => (
            <StatCard
              key={key}
              valueKey={key}
              title={title}
              Icon={Icon}
              gradient={gradient}
              item={stats[key]}
            />
          ))}
        </section>
      )}
    </>
  );
}
