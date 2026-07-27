import Chart from 'react-apexcharts';

import {
  usePatientGrowth,
  useRevenueAnalytics,
  useAppointmentsAnalytics,
  useDepartmentDistribution,
  useBedOccupancy,
  useAdmissionsAnalytics,
} from '../hooks/useDashboard';
import Loading from '../../../components/common/Loading';

const COLORS = ['#2563eb', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function formatAxisLabel(label) {
  if (!label) return label;
  const parts = String(label).split('-');

  if (parts.length === 2) return MONTHS[Number(parts[1]) - 1] || label;
  if (parts.length === 3) return `${Number(parts[2])}/${Number(parts[1])}`;

  return label;
}

function ChartCard({ title, loading, error, isEmpty, children }) {
  return (
    <div className="card chart-card">
      <div className="chart-card-head">
        <span className="chart-card-title">{title}</span>
      </div>

      {loading && <Loading size="sm" />}
      {error && <div className="empty-state error">{error}</div>}
      {!loading && !error && isEmpty && <div className="empty-state">No data yet.</div>}
      {!loading && !error && !isEmpty && children}
    </div>
  );
}

// ---------------------------------------------------------------------

function PatientGrowthChart() {
  const { data, loading, error } = usePatientGrowth('month');
  const points = data || [];

  const options = {
    chart: { toolbar: { show: false }, zoom: { enabled: false } },
    stroke: { curve: 'smooth', width: 3 },
    fill: { type: 'gradient', gradient: { opacityFrom: 0.5, opacityTo: 0.05 } },
    colors: ['#2563eb'],
    dataLabels: { enabled: false },
    xaxis: {
      categories: points.map((x) => x.label),
      labels: { formatter: formatAxisLabel },
    },
    grid: { borderColor: '#e2e8f0' },
  };

  const series = [{ name: 'Patients', data: points.map((x) => x.value) }];

  return (
    <ChartCard title="Patient Growth" loading={loading} error={error} isEmpty={!points.length}>
      <Chart options={options} series={series} type="area" height={280} />
    </ChartCard>
  );
}

// ---------------------------------------------------------------------

function RevenueChart() {
  const { data, loading, error } = useRevenueAnalytics('year');
  const points = data || [];

  const options = {
    chart: { toolbar: { show: false } },
    stroke: { curve: 'smooth', width: 3 },
    colors: ['#10b981'],
    dataLabels: { enabled: false },
    xaxis: {
      categories: points.map((x) => x.label),
      labels: { formatter: formatAxisLabel },
    },
    grid: { borderColor: '#e2e8f0' },
  };

  const series = [{ name: 'Revenue', data: points.map((x) => x.value) }];

  return (
    <ChartCard title="Revenue" loading={loading} error={error} isEmpty={!points.length}>
      <Chart options={options} series={series} type="line" height={280} />
    </ChartCard>
  );
}

// ---------------------------------------------------------------------

function DepartmentsChart() {
  const { data, loading, error } = useDepartmentDistribution();
  const departments = data || [];

  const options = {
    labels: departments.map((x) => x.department_name),
    legend: { position: 'bottom' },
    colors: COLORS,
    dataLabels: { enabled: true },
  };

  const series = departments.map((x) => x.patient_count);

  return (
    <ChartCard title="Departments" loading={loading} error={error} isEmpty={!departments.length}>
      <Chart options={options} series={series} type="donut" height={300} />
    </ChartCard>
  );
}

// ---------------------------------------------------------------------

function AppointmentsChart() {
  const { data, loading, error } = useAppointmentsAnalytics('month');

  const options = {
    chart: { toolbar: { show: false } },
    colors: ['#2563eb'],
    plotOptions: { bar: { borderRadius: 6, columnWidth: '45%' } },
    dataLabels: { enabled: false },
    xaxis: { categories: ['Scheduled', 'Completed', 'Cancelled'] },
  };

  const series = [
    {
      name: 'Appointments',
      data: [data?.scheduled || 0, data?.completed || 0, data?.cancelled || 0],
    },
  ];

  return (
    <ChartCard title="Appointments" loading={loading} error={error} isEmpty={!data}>
      <Chart options={options} series={series} type="bar" height={280} />
    </ChartCard>
  );
}

// ---------------------------------------------------------------------

function BedOccupancyChart() {
  const { data, loading, error } = useBedOccupancy('month');
  const points = data || [];

  const options = {
    chart: { toolbar: { show: false } },
    stroke: { curve: 'smooth', width: 3 },
    colors: ['#ef4444'],
    dataLabels: { enabled: false },
    xaxis: {
      categories: points.map((x) => x.label),
      labels: { formatter: formatAxisLabel },
    },
    yaxis: { max: 100 },
    grid: { borderColor: '#e2e8f0' },
  };

  const series = [{ name: 'Occupancy %', data: points.map((x) => x.occupancy_rate) }];

  return (
    <ChartCard title="Bed Occupancy" loading={loading} error={error} isEmpty={!points.length}>
      <Chart options={options} series={series} type="line" height={280} />
    </ChartCard>
  );
}

// ---------------------------------------------------------------------

function AdmissionsChart() {
  const { data, loading, error } = useAdmissionsAnalytics('month');
  const points = data || [];

  const options = {
    chart: { toolbar: { show: false } },
    plotOptions: { bar: { borderRadius: 6, columnWidth: '50%' } },
    colors: ['#2563eb', '#10b981'],
    dataLabels: { enabled: false },
    xaxis: {
      categories: points.map((x) => x.label),
      labels: { formatter: formatAxisLabel },
    },
  };

  const series = [
    { name: 'Admissions', data: points.map((x) => x.admissions) },
    { name: 'Discharges', data: points.map((x) => x.discharges) },
  ];

  return (
    <ChartCard title="Admissions" loading={loading} error={error} isEmpty={!points.length}>
      <Chart options={options} series={series} type="bar" height={280} />
    </ChartCard>
  );
}

// ---------------------------------------------------------------------

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
