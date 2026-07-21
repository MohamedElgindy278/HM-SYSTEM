import { HeartPulse } from 'lucide-react';

export default function AuthBrandPanel() {
  return (
    <div className="brand-panel">
      <div className="grid-overlay" />

      <div className="brand-top">
        <div className="brand-mark">
          <HeartPulse size={28} strokeWidth={2} color="#fff" />
        </div>
        <div className="brand-name">
          MedCore <span className="brand-highlight">HMS</span>
        </div>
      </div>

      <div className="brand-middle">
        <div className="eyebrow">
          <span className="eyebrow-dot" /> Hospital Managment System
        </div>

        <h1 className="headline">
          Care coordination, <span className="headline-gradient">simplified</span> for every
          department.
        </h1>

        <p className="brand-description">
          One secure workspace for doctors, nurses, pharmacists, and administrative staff — patient
          records, scheduling, billing, and lab results, unified in real time across your entire
          hospital network.
        </p>

        <div className="brand-stats">
          <div>
            <div className="stat-number">128+</div>
            <div className="stat-label">Hospitals&nbsp;onboarded</div>
          </div>
          <div className="stat-divider" />
          <div>
            <div className="stat-number">99.98%</div>
            <div className="stat-label">Platform&nbsp;uptime</div>
          </div>
          <div className="stat-divider" />
          <div>
            <div className="stat-number">24/7</div>
            <div className="stat-label">Clinical&nbsp;support</div>
          </div>
        </div>

        <div className="ecg-wrapper">
          <svg
            viewBox="0 0 400 60"
            preserveAspectRatio="none"
            style={{ display: 'block', width: '100%', height: 52 }}
          >
            <path
              d="M0,30 L60,30 L80,30 L95,10 L110,50 L125,4 L140,50 L155,30 L180,30 L400,30"
              className="ecg-path"
            />
          </svg>
          <div className="ecg-caption">
            Live system heartbeat — all clinical services operational
          </div>
        </div>
      </div>

      <div className="brand-bottom">
        <span>© 2026 MedCore Health Systems</span>
        <div className="brand-bottom-right">
          <div className="trust-badge">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="trust-icon"
            >
              <path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6l8-4z" />
            </svg>
            HIPAA Compliant
          </div>
          <div className="trust-badge">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="trust-icon"
            >
              <rect x="4" y="10" width="16" height="10" rx="2" />
              <path d="M8 10V7a4 4 0 0 1 8 0v3" />
            </svg>
            256-bit Encrypted
          </div>
        </div>
      </div>
    </div>
  );
}
