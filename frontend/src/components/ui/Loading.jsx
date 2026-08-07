import './Loading.css';

/**
 * Universal loading indicator used across the whole app.
 *
 * @param {'sm'|'md'|'lg'} size - sm: inline inside a small card/chart,
 *   md (default): a section loading (stat card, table, list),
 *   lg: a full page/full-panel loading state.
 * @param {string} [label] - optional text next to the spinner
 * @param {boolean} [fullHeight] - centers the spinner in a tall
 *   min-height block, for full-page/full-panel loading states
 */
export default function Loading({ size = 'md', label, fullHeight = false }) {
  return (
    <div className={`loading loading-${size}${fullHeight ? ' loading-full' : ''}`}>
      <div className="loading-spinner" />
      {label && <span className="loading-label">{label}</span>}
    </div>
  );
}
