import React from 'react';
import { Shield, Activity } from 'lucide-react';

interface NavbarProps {
  systemStatus: string;
  totalRepos: number;
}

export const Navbar: React.FC<NavbarProps> = ({ systemStatus, totalRepos }) => {
  return (
    <header className="glass-panel navbar-header">
      <div className="container navbar-container">
        {/* Brand Logo */}
        <div className="navbar-brand">
          <div className="navbar-logo-icon" style={{ background: 'conic-gradient(from 130deg, #3BE6C2, #2C5CC5, #3BE6C2)' }}>
            <Shield size={22} color="#0D1110" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
              <h1 style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '-0.02em', margin: 0 }}>
                PRAXIA<span style={{ color: '#3BE6C2' }}>.ai</span>
              </h1>
              <span className="badge badge-info" style={{ fontSize: '0.65rem', padding: '2px 8px', background: 'rgba(59, 230, 194, 0.15)', color: '#3BE6C2', border: '1px solid rgba(59, 230, 194, 0.3)' }}>v2.0 RAG & DeepCode</span>
            </div>
            <p className="navbar-tagline" style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0 }}>
              Autonomous Code Auditing & AI Opportunity Assessment
            </p>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="navbar-status-group">
          <div className="navbar-status-pill">
            <span
              className="navbar-status-dot animate-pulse-slow"
              style={{
                backgroundColor: systemStatus === 'healthy' ? 'var(--accent-emerald)' : 'var(--accent-amber)',
                boxShadow: systemStatus === 'healthy' ? '0 0 10px var(--accent-emerald)' : 'none',
              }}
            />
            <span style={{ color: 'var(--text-secondary)' }}>RAG & LLM:</span>
            <span style={{ fontWeight: 600, color: systemStatus === 'healthy' ? 'var(--accent-emerald)' : 'var(--accent-amber)' }}>
              {systemStatus === 'healthy' ? 'ONLINE' : 'CONNECTING'}
            </span>
          </div>

          <div className="navbar-status-pill">
            <Activity size={14} color="var(--accent-indigo)" />
            <span style={{ color: 'var(--text-secondary)' }}>Repos:</span>
            <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{totalRepos}</span>
          </div>
        </div>
      </div>
    </header>
  );
};
