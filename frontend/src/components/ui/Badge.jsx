const TONE_CLASS = {
  success: 'b-success',
  danger: 'b-danger',
  warning: 'b-warning',
  info: 'b-info',
};

export default function Badge({ tone = 'info', children, dot = true, className = '' }) {
  return (
    <span className={`badge ${TONE_CLASS[tone] || TONE_CLASS.info} ${className}`.trim()}>
      {dot && <span className="bdot" />}
      {children}
    </span>
  );
}
