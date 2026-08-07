import { Component } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // في المستقبل: ابعت لـ logging service (Sentry / LogRocket)
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  handleReload = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            minHeight: '60vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 16,
            padding: 32,
            textAlign: 'center',
            fontFamily: 'var(--font-family, system-ui)',
            color: 'var(--color-text, #475569)',
          }}
        >
          <div
            style={{
              width: 64,
              height: 64,
              borderRadius: '50%',
              background: 'var(--color-danger-bg, #fef2f2)',
              color: 'var(--color-danger-text, #b91c1c)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <AlertTriangle size={28} />
          </div>

          <h2 style={{ margin: 0, color: 'var(--color-title, #0f172a)', fontSize: 20 }}>
            Something went wrong
          </h2>

          <p style={{ margin: 0, maxWidth: 360, lineHeight: 1.5 }}>
            An unexpected error occurred. You can try reloading the page.
          </p>

          {import.meta.env.DEV && this.state.error && (
            <pre
              style={{
                maxWidth: 480,
                overflow: 'auto',
                padding: 12,
                background: '#f1f5f9',
                borderRadius: 8,
                fontSize: 12,
                textAlign: 'left',
              }}
            >
              {this.state.error.toString()}
            </pre>
          )}

          <button
            type="button"
            onClick={this.handleReload}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              padding: '10px 18px',
              border: 'none',
              borderRadius: 8,
              background: 'var(--color-primary, #2563eb)',
              color: '#fff',
              fontWeight: 600,
              cursor: 'pointer',
              fontFamily: 'inherit',
            }}
          >
            <RefreshCw size={16} />
            Reload page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
