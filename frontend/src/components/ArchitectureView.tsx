import React from 'react';
import { Layers, AlertOctagon, CheckCircle2, ArrowRight } from 'lucide-react';
import { ArchitectureData } from '../services/api';

interface ArchitectureViewProps {
  architecture: ArchitectureData | null;
}

export const ArchitectureView: React.FC<ArchitectureViewProps> = ({ architecture }) => {
  if (!architecture) {
    return (
      <div className="border border-border-subtle bg-surface p-12 text-center flex flex-col items-center justify-center gap-3">
        <Layers className="size-10 text-text-muted" />
        <h3 className="font-sans text-base font-bold text-text">Sin análisis arquitectónico disponible</h3>
        <p className="font-mono text-xs text-text-muted max-w-md">
          Ejecuta una auditoría sobre el repositorio para generar y visualizar el grafo de dependencias y análisis acíclico.
        </p>
      </div>
    );
  }

  const hasCycles = architecture.has_circular_dependencies;
  const cycles = architecture.ciclos_detectados || [];

  return (
    <div className="space-y-6">
      {/* Overview Card */}
      <div className="border border-border-subtle bg-surface/90 hover:border-border-strong p-6 transition-colors duration-150">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border-subtle">
          <div className="flex items-center gap-3">
            <div className="p-2 border border-brand/30 bg-brand-soft text-brand">
              <Layers className="size-5" />
            </div>
            <div>
              <h2 className="font-sans text-lg font-bold tracking-tight text-text">
                Resumen de Arquitectura y Grafo de Módulos
              </h2>
              <p className="font-mono text-xs text-text-muted mt-0.5">{architecture.resumen}</p>
            </div>
          </div>

          <span
            className={`font-mono text-xs px-3 py-1 border uppercase tracking-wider font-semibold flex-shrink-0 ${
              hasCycles
                ? 'border-rose-500/40 bg-rose-950/40 text-rose-300'
                : 'border-emerald-500/40 bg-emerald-950/40 text-emerald-300'
            }`}
          >
            {hasCycles ? 'Dependencias Circulares Detectadas' : 'Grafo Acíclico (DAG)'}
          </span>
        </div>

        {/* Circular Dependency Warning Alert */}
        {hasCycles ? (
          <div className="border border-rose-500/30 bg-rose-950/20 p-5 mt-4 space-y-3">
            <div className="flex items-center gap-2 text-rose-300">
              <AlertOctagon className="size-5 flex-shrink-0 text-rose-400" />
              <h3 className="font-sans font-bold text-sm text-rose-200">
                Alerta Arquitectónica: Ciclos de Importación Detectados ({cycles.length})
              </h3>
            </div>
            <p className="font-sans text-xs text-text-secondary leading-relaxed">
              Los siguientes módulos forman bucles cerrados de dependencia. Esto viola el principio{' '}
              <strong className="text-text font-mono">Acyclic Dependencies Principle (ADP)</strong> y bloquea el desacoplamiento:
            </p>

            <div className="flex flex-col gap-2 mt-2">
              {cycles.map((cycle, idx) => (
                <div
                  key={idx}
                  className="border border-border-subtle bg-bg-deep/90 p-3 font-mono text-xs text-text flex items-center gap-2 flex-wrap"
                >
                  {cycle.map((mod, mIdx) => (
                    <React.Fragment key={mIdx}>
                      <span
                        className={
                          mIdx === 0 || mIdx === cycle.length - 1
                            ? 'text-rose-400 font-semibold'
                            : 'text-text-secondary'
                        }
                      >
                        {mod}
                      </span>
                      {mIdx < cycle.length - 1 && <ArrowRight className="size-3.5 text-brand" />}
                    </React.Fragment>
                  ))}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="border border-emerald-500/30 bg-emerald-950/20 p-4 mt-4 flex items-center gap-3">
            <CheckCircle2 className="size-5 text-emerald-400 flex-shrink-0" />
            <span className="font-mono text-xs text-emerald-200">
              No se detectaron dependencias circulares. La dirección del flujo entre capas respeta el orden topológico acíclico.
            </span>
          </div>
        )}
      </div>
    </div>
  );
};
