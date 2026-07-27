import './Loading.css';

export default function Loading({ size = 'md', label, fullHeight = false }) {
  return (
    <div className={`loading loading-${size}${fullHeight ? ' loading-full' : ''}`}>
      <div className="loading-spinner" />
      {label && <span className="loading-label">{label}</span>}
    </div>
  );
}
