import { useEffect } from 'react';
import { AlertTriangle } from 'lucide-react';

import Button from './Button';
import './ConfirmDialog.css';

/**
 * Shared confirmation modal used across the app instead of window.confirm()
 * (e.g. "Delete patient?", "Cancel appointment?").
 *
 * @param {boolean} open
 * @param {string} [title='Are you sure?']
 * @param {string} [message] - optional supporting text
 * @param {string} [confirmLabel='Confirm']
 * @param {string} [cancelLabel='Cancel']
 * @param {'danger'|'primary'} [variant='danger']
 * @param {boolean} [loading=false] - shows a spinner on the confirm button
 *   and disables both buttons + the Escape/overlay-click dismissal
 * @param {() => void} onConfirm
 * @param {() => void} onCancel
 */
export default function ConfirmDialog({
  open,
  title = 'Are you sure?',
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  variant = 'danger',
  loading = false,
  onConfirm,
  onCancel,
}) {
  useEffect(() => {
    if (!open) return;

    const handleKeyDown = (event) => {
      if (event.key === 'Escape' && !loading) onCancel?.();
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [open, loading, onCancel]);

  if (!open) return null;

  return (
    <div className="confirm-overlay" onClick={() => !loading && onCancel?.()}>
      <div
        className="confirm-dialog"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="confirm-dialog-title"
        onClick={(event) => event.stopPropagation()}
      >
        <div className={`confirm-icon confirm-icon-${variant}`}>
          <AlertTriangle size={22} />
        </div>

        <h3 className="confirm-title" id="confirm-dialog-title">
          {title}
        </h3>

        {message && <p className="confirm-message">{message}</p>}

        <div className="confirm-actions">
          <Button variant="outline" onClick={onCancel} disabled={loading}>
            {cancelLabel}
          </Button>

          <Button
            variant={variant === 'danger' ? 'danger' : 'primary'}
            onClick={onConfirm}
            loading={loading}
          >
            {confirmLabel}
          </Button>
        </div>
      </div>
    </div>
  );
}
