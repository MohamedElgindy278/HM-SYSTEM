import { ChevronDown } from 'lucide-react';

const REVENUE_BARS = [
  { month: 'Feb', height: 52 },
  { month: 'Mar', height: 64 },
  { month: 'Apr', height: 48 },
  { month: 'May', height: 74 },
  { month: 'Jun', height: 60 },
  { month: 'Jul', height: 88 },
];

const ADMISSIONS_BARS = [
  { month: 'Feb', height: 40 },
  { month: 'Mar', height: 58 },
  { month: 'Apr', height: 50 },
  { month: 'May', height: 70 },
  { month: 'Jun', height: 66 },
  { month: 'Jul', height: 80 },
];

const DEPARTMENTS = [
  { label: 'Cardiology', color: '#2563EB' },
  { label: 'Pediatrics', color: '#06B6D4' },
  { label: 'Orthopedics', color: '#10B981' },
  { label: 'Neurology', color: '#F59E0B' },
  { label: 'General', color: '#0EA5E9' },
];

const OCCUPANCY = [
  { label: 'ICU', pct: 84, color: '#EF4444' },
  { label: 'General Ward', pct: 61, color: '#2563EB' },
  { label: 'Maternity', pct: 45, color: '#06B6D4' },
  { label: 'Pediatric', pct: 38, color: '#10B981' },
];

function ChartCard({ title, period, children }) {
  return (
    <div className="card">
      <div className="chart-card-head">
        <span className="chart-card-title">{title}</span>
        {period && (
          <span className="chart-period">
            {period} <ChevronDown size={12} strokeWidth={2} />
          </span>
        )}
      </div>
      {children}
    </div>
  );
}

function BarChart({ data, color1, color2 }) {
  return (
    <div className="bars">
      {data.map((bar) => (
        <div className="bar-col" key={bar.month}>
          <div
            className="bar"
            style={{
              height: `${bar.height}%`,
              background: `linear-gradient(180deg, ${color1}, ${color2})`,
            }}
          />
          <span className="bar-mo">{bar.month}</span>
        </div>
      ))}
    </div>
  );
}

export default function Analytics() {
  return (
    <>
      <h2 className="section-title">Analytics</h2>
      <div className="grid grid-analytics">
        <ChartCard title="Patients Growth" period="Last 30 days">
          <svg viewBox="0 0 400 150" preserveAspectRatio="none" className="area-chart">
            <path
              d="M0,110 C40,90 60,120 100,95 C140,70 160,105 200,80 C240,55 260,90 300,60 C330,38 360,50 400,20 L400,150 L0,150 Z"
              fill="#2563EB"
              opacity={0.08}
            />
            <path
              d="M0,110 C40,90 60,120 100,95 C140,70 160,105 200,80 C240,55 260,90 300,60 C330,38 360,50 400,20"
              fill="none"
              stroke="#2563EB"
              strokeWidth={2.5}
              strokeLinecap="round"
            />
          </svg>
        </ChartCard>

        <ChartCard title="Revenue" period="This year">
          <BarChart data={REVENUE_BARS} color1="#2563EB" color2="#3B82F6" />
        </ChartCard>

        <ChartCard title="Appointments">
          <svg viewBox="0 0 400 140" preserveAspectRatio="none" className="line-chart">
            <path
              d="M0,90 C50,80 90,100 140,70 C180,48 220,75 260,55 C300,38 340,60 400,30"
              fill="none"
              stroke="#2563EB"
              strokeWidth={2.5}
              strokeLinecap="round"
            />
            <path
              d="M0,110 C50,115 90,105 140,112 C180,118 220,108 260,113 C300,116 340,106 400,110"
              fill="none"
              stroke="#EF4444"
              strokeWidth={2.5}
              strokeLinecap="round"
            />
          </svg>
          <div className="chart-legend">
            <span className="legend-item">
              <span className="legend-dot c1" />
              Completed
            </span>
            <span className="legend-item">
              <span className="legend-dot" style={{ background: '#EF4444' }} />
              Cancelled
            </span>
          </div>
        </ChartCard>

        <ChartCard title="Departments Distribution">
          <div
            className="donut-wrap"
            style={{
              background:
                'conic-gradient(#2563EB 0 28%, #06B6D4 28% 47%, #10B981 47% 64%, #F59E0B 64% 79%, #0EA5E9 79% 91%, #CBD5E1 91% 100%)',
            }}
          >
            <div className="donut-center">
              <div className="donut-value">1,284</div>
              <div className="donut-label">Total Patients</div>
            </div>
          </div>
          <div className="chart-legend">
            {DEPARTMENTS.map((dep) => (
              <span className="legend-item" key={dep.label}>
                <span className="legend-dot" style={{ background: dep.color }} />
                {dep.label}
              </span>
            ))}
          </div>
        </ChartCard>

        <ChartCard title="Bed Occupancy">
          {OCCUPANCY.map((row) => (
            <div className="gauge-row" key={row.label}>
              <span className="gauge-label">{row.label}</span>
              <div className="gauge-track">
                <div
                  className="gauge-fill"
                  style={{ width: `${row.pct}%`, background: row.color }}
                />
              </div>
              <span className="gauge-pct">{row.pct}%</span>
            </div>
          ))}
        </ChartCard>

        <ChartCard title="Monthly Admissions">
          <BarChart data={ADMISSIONS_BARS} color1="#06B6D4" color2="#22D3EE" />
        </ChartCard>
      </div>
    </>
  );
}
