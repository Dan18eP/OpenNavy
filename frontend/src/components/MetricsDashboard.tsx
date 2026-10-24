import React from 'react';
import { 
  Gauge, 
  GitFork, 
  Box, 
  Copy, 
  CheckCircle, 
  Layers, 
  Sparkles, 
  TrendingDown,
  Boxes,
  ExternalLink
} from 'lucide-react';
import { MetricItem } from '../services/api';

interface MetricsDashboardProps {
  metrics: MetricItem[];
  onOpenDependencies?: () => void;
}

interface CriterionConfig {
  id: string;
  name: string;
  weight: string;
  description: string;
  icon: React.ReactNode;
  unit: string;
  target: string;
}

const CRITERIA_CONFIGS: Record<string, CriterionConfig> = {
  maintainability_index: {
    id: 'maintainability_index',
    name: 'Índice de Mantenibilidad',
    weight: '15%',
    description: 'Fórmula Halstead / McCabe / LOC. Mide facilidad de cambio.',
    icon: <Gauge size={18} color="var(--accent-indigo)" />,
    unit: '/ 100',
    target: '≥ 65',
  },
  cyclomatic_complexity: {
    id: 'cyclomatic_complexity',
    name: 'Complejidad Ciclomática',
    weight: '15%',
    description: 'Conteo de nodos de decisión McCabe por función.',
    icon: <GitFork size={18} color="var(--accent-violet)" />,
    unit: 'score',
    target: '≤ 10 / func',
  },
  solid_principles: {
    id: 'solid_principles',
    name: 'Principios SOLID',
    weight: '15%',
    description: 'Evaluación de SRP, OCP, LSP, ISP, DIP contra rúbrica RAG.',
    icon: <Box size={18} color="var(--accent-cyan)" />,
    unit: 'salud',
    target: '0 críticas',
  },
  code_duplication: {
    id: 'code_duplication',
    name: 'Duplicación de Código',
    weight: '10%',
    description: 'Hashing de subárboles sintácticos (Clones Tipo 1 y 2).',
    icon: <Copy size={18} color="var(--accent-amber)" />,
    unit: '% dup',
    target: '< 5%',
  },
  test_coverage: {
    id: 'test_coverage',
    name: 'Cobertura de Pruebas',
    weight: '15%',
    description: 'Reportes de cobertura de líneas y ramas ejecutadas.',
    icon: <CheckCircle size={18} color="var(--accent-emerald)" />,
    unit: '% cov',
    target: '≥ 80%',
  },
  architecture: {
    id: 'architecture',
    name: 'Directrices Arquitectura',
    weight: '15%',
    description: 'Grafo de dependencias y detección de ciclos circulares.',
    icon: <Layers size={18} color="#ec4899" />,
    unit: 'salud',
    target: '0 ciclos',
  },
  clean_code: {
    id: 'clean_code',
    name: 'Estándares Clean Code',
    weight: '5%',
    description: 'Nomenclatura semántica, tamaño y control de efectos secundarios.',
    icon: <Sparkles size={18} color="#f43f5e" />,
    unit: 'salud',
    target: 'Sin advertencias',
  },
  dependency_version_control: {
    id: 'dependency_version_control',
    name: 'Control de Versiones y Dependencias',
    weight: '10%',
    description: 'Análisis SemVer, detección de obsolescencia, incompatibilidades y propuestas.',
    icon: <Boxes size={18} color="#6366f1" />,
    unit: 'salud',
    target: '≥ 80%',
  },
  defect_density: {
    id: 'defect_density',
    name: 'Métricas DORA / Proceso',
    weight: 'Integración',
    description: 'Tasa de fallos y densidad de defectos (conectar tracker).',
    icon: <TrendingDown size={18} color="var(--text-muted)" />,
    unit: 'KLOC',
    target: '< 1 def/KLOC',
  },
};

export const MetricsDashboard: React.FC<MetricsDashboardProps> = ({ metrics, onOpenDependencies }) => {
  const metricsMap = new Map(metrics.map((m) => [m.criterio, m.valor]));

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 700 }}>Desglose de los Criterios de Calidad y Dependencias</h3>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Métricas calculadas por AST, analizadores de dependencias, grafos y evaluación RAG</p>
        </div>

        {onOpenDependencies && (
          <button
            onClick={onOpenDependencies}
            className="btn btn-secondary"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '0.8rem',
              padding: '8px 14px',
              borderColor: 'rgba(99, 102, 241, 0.4)',
              background: 'rgba(99, 102, 241, 0.1)',
              color: '#c7d2fe',
            }}
          >
            <Boxes size={16} />
            Auditar Dependencias & Propuestas
          </button>
        )}
      </div>

      <div className="metrics-grid">
        {Object.entries(CRITERIA_CONFIGS).map(([key, config]) => {
          const value = metricsMap.get(key) ?? 75.0;
          const isHealthy = value >= 70;
          const isWarning = value >= 50 && value < 70;
          const statusColor = isHealthy ? 'var(--accent-emerald)' : isWarning ? 'var(--accent-amber)' : 'var(--accent-rose)';
          const isDependencyCard = key === 'dependency_version_control';

          return (
            <div 
              key={key} 
              className="glass-card" 
              style={{ 
                padding: '20px', 
                display: 'flex', 
                flexDirection: 'column', 
                justifyContent: 'space-between',
                border: isDependencyCard ? '1px solid rgba(99, 102, 241, 0.35)' : undefined,
                background: isDependencyCard ? 'linear-gradient(135deg, rgba(30, 27, 75, 0.4), rgba(17, 24, 39, 0.8))' : undefined,
              }}
            >
              <div>
                {/* Card Header */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <div style={{ background: 'rgba(255, 255, 255, 0.04)', padding: '8px', borderRadius: '10px', display: 'flex' }}>
                      {config.icon}
                    </div>
                    <div>
                      <h4 style={{ fontSize: '0.92rem', fontWeight: 700 }}>{config.name}</h4>
                      <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Peso: {config.weight}</span>
                    </div>
                  </div>

                  <span style={{ fontSize: '1.25rem', fontWeight: 800, color: statusColor }}>
                    {value.toFixed(1)}
                  </span>
                </div>

                <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '14px', lineHeight: 1.5 }}>
                  {config.description}
                </p>

                {isDependencyCard && onOpenDependencies && (
                  <button
                    onClick={onOpenDependencies}
                    style={{
                      background: 'rgba(99, 102, 241, 0.15)',
                      border: '1px solid rgba(99, 102, 241, 0.3)',
                      color: '#c7d2fe',
                      padding: '5px 10px',
                      borderRadius: '6px',
                      fontSize: '0.74rem',
                      fontWeight: 600,
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '5px',
                      marginBottom: '12px',
                    }}
                  >
                    <span>Ver paquetes & propuestas</span>
                    <ExternalLink size={12} />
                  </button>
                )}
              </div>

              {/* Progress & Target */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
                  <span>Objetivo: {config.target}</span>
                  <span style={{ color: statusColor, fontWeight: 600 }}>{value.toFixed(0)}%</span>
                </div>
                <div style={{ width: '100%', height: '6px', background: 'rgba(0, 0, 0, 0.3)', borderRadius: '9999px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${Math.min(100, Math.max(0, value))}%`,
                      height: '100%',
                      backgroundColor: statusColor,
                      transition: 'width 0.4s ease',
                    }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

