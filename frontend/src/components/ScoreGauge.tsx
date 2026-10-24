import React from 'react';
import { FileDown, Loader2 } from 'lucide-react';

interface ScoreGaugeProps {
  score: number | null;
  lastAnalyzedAt?: string;
  totalFindings: number;
  onDownloadPdf?: () => void;
  isDownloadingPdf?: boolean;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ 
  score, 
  lastAnalyzedAt, 
  totalFindings,
  onDownloadPdf,
  isDownloadingPdf,
}) => {
  const currentScore = score ?? 0;
  const isHealthy = currentScore >= 80;
  const isWarning = currentScore >= 60 && currentScore < 80;

  const color = isHealthy ? 'var(--accent-emerald)' : isWarning ? 'var(--accent-amber)' : 'var(--accent-rose)';
  const statusLabel = isHealthy ? 'Excelente / Saludable' : isWarning ? 'Riesgo Moderado' : 'Deuda Técnica Crítica';

  // SVG Circular Gauge calculation
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (currentScore / 100) * circumference;

  return (
    <div className="glass-card score-gauge-card">
      <div className="score-gauge-layout">
        {/* Left Info */}
        <div className="score-gauge-info">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', flexWrap: 'wrap' }}>
            <span className={`badge ${isHealthy ? 'badge-success' : isWarning ? 'badge-warning' : 'badge-critical'}`}>
              {statusLabel}
            </span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              {lastAnalyzedAt ? `Actualizado: ${new Date(lastAnalyzedAt).toLocaleTimeString()}` : 'Listo para escanear'}
            </span>
          </div>

          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: '8px', letterSpacing: '-0.02em', margin: 0 }}>
            Score Global de Salud
          </h2>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', maxWidth: '480px', lineHeight: 1.6, margin: '8px 0 0' }}>
            Puntaje ponderado de los 8 criterios de calidad (SOLID, Complejidad Ciclomática, Mantenibilidad, Duplicación, Arquitectura y Clean Code).
          </p>

          <div className="score-gauge-actions">
            <div className="score-stat-box">
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>Hallazgos Totales</span>
              <span style={{ fontSize: '1.2rem', fontWeight: 700, color: totalFindings > 0 ? 'var(--accent-amber)' : 'var(--accent-emerald)' }}>
                {totalFindings}
              </span>
            </div>

            <div className="score-stat-box">
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>Umbral Aceptable</span>
              <span style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                ≥ 70 / 100
              </span>
            </div>

            {score !== null && onDownloadPdf && (
              <button
                onClick={onDownloadPdf}
                disabled={isDownloadingPdf}
                className="btn-secondary score-pdf-btn"
              >
                {isDownloadingPdf ? (
                  <>
                    <Loader2 size={16} className="animate-spin" color="var(--accent-indigo)" />
                    <span>Generando PDF...</span>
                  </>
                ) : (
                  <>
                    <FileDown size={16} color="var(--accent-indigo)" />
                    <span>Descargar Informe PDF</span>
                  </>
                )}
              </button>
            )}
          </div>
        </div>

        {/* Right Circular Gauge */}
        <div className="score-gauge-circle-container">
          <svg width="150" height="150" style={{ transform: 'rotate(-90deg)' }}>
            {/* Background circle */}
            <circle
              cx="75"
              cy="75"
              r={radius}
              stroke="rgba(255, 255, 255, 0.06)"
              strokeWidth="12"
              fill="transparent"
            />
            {/* Animated progress circle */}
            <circle
              cx="75"
              cy="75"
              r={radius}
              stroke={color}
              strokeWidth="12"
              fill="transparent"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              style={{ transition: 'stroke-dashoffset 0.8s ease, stroke 0.4s ease' }}
            />
          </svg>

          {/* Inner Score Number */}
          <div style={{ position: 'absolute', textAlign: 'center' }}>
            <span style={{ fontSize: '2.1rem', fontWeight: 800, color: '#ffffff', display: 'block', lineHeight: 1 }}>
              {score !== null ? score : '--'}
            </span>
            <span style={{ fontSize: '0.75rem', fontWeight: 600, color: color, textTransform: 'uppercase' }}>
              / 100 PTS
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
