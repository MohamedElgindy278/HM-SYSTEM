import { Loader2 } from 'lucide-react';

const VARIANT_CLASS = {
  primary: 'btn-primary',
  outline: 'btn-outline',
  danger: 'btn-danger',
};

/**
 * Shared button used across the whole app.
 *
 * @param {'primary'|'outline'|'danger'} [variant='primary']
 * @param {'sm'} [size] - omit for default size
 * @param {boolean} [loading=false] - shows a spinner and disables the button
 * @param {import('react').ElementType} [icon] - a lucide-react icon component
 */
export default function Button({
  children,
  variant = 'primary',
  size,
  loading = false,
  disabled = false,
  type = 'button',
  className = '',
  icon: Icon,
  ...rest
}) {
  const classes = [
    'btn',
    VARIANT_CLASS[variant] || VARIANT_CLASS.primary,
    size === 'sm' ? 'btn-sm' : '',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button type={type} className={classes} disabled={disabled || loading} {...rest}>
      {loading ? <Loader2 size={14} className="btn-spin" /> : Icon ? <Icon size={16} /> : null}
      {children}
    </button>
  );
}
