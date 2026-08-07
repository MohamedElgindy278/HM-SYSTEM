import { useState } from 'react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

import { Card } from '../../../components/ui';
import {
  usePatientGrowth,
  useRevenueAnalytics,
  useAppointmentsAnalytics,
  useDepartmentDistribution,
  useBedOccupancy,
  useAdmissionsAnalytics,
} from '../hooks/useDashboard';
import { extractErrorMessage } from '../../../utils/errors';
import PeriodSelector from './PeriodSelector';

const COLORS = ['#2563eb', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function formatAxisLabel(label) {
  if (!label) return label;
  const parts = String(label).split('-');
  if (parts.length === 2) return MONTHS[Number(parts[1]) - 1] || label;
  if (parts.length === 3) return `${Number(parts[2])}/${Number(parts[1])}`;
  return label;
}

function ChartSkeleton() {
  return <div className="skeleton skeleton-chart" />;
}

function ChartCard({
  title,
  period,
  onPeriodChange,
  isLoading,
  isError,
  error,
  isEmpty,
  children,
}) {
  return (
    <Card className="chart-card" hoverable={false}>
      <div className="chart-card-head">
        <span className="chart-card-title">{title}</span>
        {onPeriodChange && <PeriodSelector value={period} onChange={onPeriodChange} />}
      </div>

      {isLoading && <ChartSkeleton />}
      {isError && <div className="empty-state error">{extractErrorMessage(error)}</div>}
      {!isLoading && !isError && isEmpty && <div className="empty-state">No data yet.</div>}
      {!isLoading && !isError && !isEmpty && children}
    </Card>
  );
}

function PatientGrowthChart() {
  const [period, setPeriod] = useState('month');
  const { data, isLoading, isError, error } = usePatientGrowth(period);
  const points = (data || []).map((x) => ({
    label: formatAxisLabel(x.label),
    value: Number(x.value) || 0,
  }));

  return (
    <ChartCard
      title="Patient Growth"
      period={period}
      onPeriodChange={setPeriod}
      isLoading={isLoading}
      isError={isError}
      error={error}
      isEmpty={!points.length}
    >
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={points} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="patientGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#2563eb" stopOpacity={0.35} />
              <stop offset="100%" stopColor="#2563eb" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="label" tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <YAxis tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <Tooltip />
          <Area
            type="monotone"
            dataKey="value"
            name="Patients"
            stroke="#2563eb"
            strokeWidth={2.5}
            fill="url(#patientGrad)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function RevenueChart() {
  const [period, setPeriod] = useState('year');
  const { data, isLoading, isError, error } = useRevenueAnalytics(period);
  const points = (data || []).map((x) => ({
    label: formatAxisLabel(x.label),
    value: Number(x.value) || 0,
  }));

  return (
    <ChartCard
      title="Revenue"
      period={period}
      onPeriodChange={setPeriod}
      isLoading={isLoading}
      isError={isError}
      error={error}
      isEmpty={!points.length}
    >
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={points} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="label" tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <YAxis tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            name="Revenue"
            stroke="#10b981"
            strokeWidth={2.5}
            dot={{ r: 3 }}
            activeDot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function DepartmentsChart() {
  const { data, isLoading, isError, error } = useDepartmentDistribution();
  const departments = (data || []).map((x) => ({
    name: x.department_name,
    value: Number(x.patient_count) || 0,
  }));

  return (
    <ChartCard
      title="Departments"
      isLoading={isLoading}
      isError={isError}
      error={error}
      isEmpty={!departments.length}
    >
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={departments}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            innerRadius={70}
            outerRadius={110}
            paddingAngle={2}
          >
            {departments.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend verticalAlign="bottom" height={36} />
        </PieChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function AppointmentsChart() {
  const [period, setPeriod] = useState('month');
  const { data, isLoading, isError, error } = useAppointmentsAnalytics(period);

  const chartData = [
    { name: 'Scheduled', value: data?.scheduled ?? 0 },
    { name: 'Completed', value: data?.completed ?? 0 },
    { name: 'Cancelled', value: data?.cancelled ?? 0 },
  ];

  const isEmpty = !data || (data.scheduled === 0 && data.completed === 0 && data.cancelled === 0);

  return (
    <ChartCard
      title="Appointments"
      period={period}
      onPeriodChange={setPeriod}
      isLoading={isLoading}
      isError={isError}
      error={error}
      isEmpty={isEmpty}
    >
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="name" tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <YAxis tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <Tooltip />
          <Bar dataKey="value" name="Appointments" fill="#2563eb" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function BedOccupancyChart() {
  const [period, setPeriod] = useState('month');
  const { data, isLoading, isError, error } = useBedOccupancy(period);
  const points = (data || []).map((x) => ({
    label: formatAxisLabel(x.label),
    value: Number(x.value ?? x.occupancy_rate) || 0,
  }));

  return (
    <ChartCard
      title="Bed Occupancy"
      period={period}
      onPeriodChange={setPeriod}
      isLoading={isLoading}
      isError={isError}
      error={error}
      isEmpty={!points.length}
    >
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={points} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="label" tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} stroke="#94a3b8" unit="%" />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            name="Occupancy %"
            stroke="#ef4444"
            strokeWidth={2.5}
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

function AdmissionsChart() {
  const [period, setPeriod] = useState('month');
  const { data, isLoading, isError, error } = useAdmissionsAnalytics(period);
  const points = (data || []).map((x) => ({
    label: formatAxisLabel(x.label),
    admissions: Number(x.admissions) || 0,
    discharges: Number(x.discharges) || 0,
  }));

  return (
    <ChartCard
      title="Admissions"
      period={period}
      onPeriodChange={setPeriod}
      isLoading={isLoading}
      isError={isError}
      error={error}
      isEmpty={!points.length}
    >
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={points} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="label" tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <YAxis tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <Tooltip />
          <Legend />
          <Bar dataKey="admissions" name="Admissions" fill="#2563eb" radius={[4, 4, 0, 0]} />
          <Bar dataKey="discharges" name="Discharges" fill="#10b981" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartCard>
  );
}

export default function Analytics() {
  return (
    <>
      <h2 className="section-title">Analytics</h2>

      <section className="grid grid-analytics">
        <PatientGrowthChart />
        <RevenueChart />
        <DepartmentsChart />
        <AppointmentsChart />
        <BedOccupancyChart />
        <AdmissionsChart />
      </section>
    </>
  );
}
