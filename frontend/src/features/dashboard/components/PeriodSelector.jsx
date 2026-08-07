const PERIODS = [
  { value: 'week', label: 'Week' },
  { value: 'month', label: 'Month' },
  { value: 'year', label: 'Year' },
];

export default function PeriodSelector({ value = 'month', onChange }) {
  return (
    <div className="period-selector" role="group" aria-label="Select period">
      {PERIODS.map((p) => (
        <button
          key={p.value}
          type="button"
          className={`period-btn ${value === p.value ? 'active' : ''}`}
          onClick={() => onChange?.(p.value)}
          aria-pressed={value === p.value}
        >
          {p.label}
        </button>
      ))}
    </div>
  );
}
