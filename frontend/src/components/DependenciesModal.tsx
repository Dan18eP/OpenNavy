import React, { useState } from 'react';
import { 
  X, 
  Boxes, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldAlert, 
  ArrowUpCircle, 
  RefreshCw, 
  Copy, 
  Check, 
  Filter
} from 'lucide-react';
import { DependencyAuditResponse, DependencyItem } from '../services/api';

interface DependenciesModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: DependencyAuditResponse | null;
  isLoading?: boolean;
}

export const DependenciesModal: React.FC<DependenciesModalProps> = ({
  isOpen,
  onClose,
  data,
  isLoading = false,
}) => {
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  if (!isOpen) return null;

  const dependencies: DependencyItem[] = data?.dependencies || [];

  const filteredDeps = dependencies.filter((dep) => {
    if (filterStatus === 'incompatible') return dep.status === 'incompatible';
    if (filterStatus === 'outdated') return dep.status !== 'up_to_date';
    if (filterStatus === 'up_to_date') return dep.status === 'up_to_date';
    if (filterStatus === 'major') return dep.status === 'major_update';
    return true;
  });

  const handleCopyCommand = (command: string, index: number) => {
    if (!command) return;
    navigator.clipboard.writeText(command);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'incompatible':
        return (
          <span className="inline-flex items-center gap-1.5 font-mono text-[11px] font-bold px-2 py-0.5 border border-rose-500/40 bg-rose-950/40 text-rose-300 uppercase">
            <ShieldAlert className="size-3 text-rose-400" /> Incompatible
          </span>
        );
      case 'major_update':
        return (
          <span className="inline-flex items-center gap-1.5 font-mono text-[11px] font-semibold px-2 py-0.5 border border-rose-500/30 bg-rose-950/20 text-rose-400 uppercase">
            <AlertTriangle className="size-3 text-rose-400" /> Major Update
          </span>
        );
      case 'minor_update':
        return (
          <span className="inline-flex items-center gap-1.5 font-mono text-[11px] font-semibold px-2 py-0.5 border border-amber-500/40 bg-amber-950/40 text-amber-300 uppercase">
            <ArrowUpCircle className="size-3 text-amber-400" /> Minor Update
          </span>
        );
      case 'patch_update':
        return (
          <span className="inline-flex items-center gap-1.5 font-mono text-[11px] font-semibold px-2 py-0.5 border border-cyan-500/40 bg-cyan-950/40 text-cyan-300 uppercase">
            <RefreshCw className="size-3 text-cyan-400" /> Patch
          </span>
        );
      case 'up_to_date':
      default:
        return (
          <span className="inline-flex items-center gap-1.5 font-mono text-[11px] font-semibold px-2 py-0.5 border border-emerald-500/40 bg-emerald-950/40 text-emerald-300 uppercase">
            <CheckCircle2 className="size-3 text-emerald-400" /> Al Día
          </span>
        );
    }
  };

  const scoreVal = data?.score ?? 100.0;
  const isHealthy = scoreVal >= 80;
  const isWarning = scoreVal >= 50 && scoreVal < 80;
  const scoreColor = isHealthy ? 'text-emerald-400' : isWarning ? 'text-amber-400' : 'text-rose-400';

  return (
    <div
      className="fixed inset-0 bg-black/75 backdrop-blur-md z-[9999] flex items-center justify-center p-4 animate-fadeIn"
      onClick={onClose}
    >
      <div
        className="w-full max-w-4xl max-h-[90vh] flex flex-col border border-border-strong bg-surface ring-elevation overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-5 px-6 border-b border-border-subtle bg-surface-2/40">
          <div className="flex items-center gap-3">
            <div className="p-2 border border-brand/40 bg-brand-soft text-brand">
              <Boxes className="size-5" />
            </div>
            <div>
              <h3 className="font-sans text-base font-bold text-text">
                Auditoría de Control de Versiones y Dependencias
              </h3>
              <p className="font-mono text-xs text-text-muted mt-0.5">
                Detección de compatibilidad, obsolescencia y propuestas de actualización
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="text-text-muted hover:text-text p-1 transition-colors"
          >
            <X className="size-5" />
          </button>
        </div>

        {/* Top Summary Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 p-4 px-6 border-b border-border-subtle bg-bg-deep/80">
          <div className="p-3 border border-border-subtle bg-surface/60">
            <span className="font-mono text-[10px] text-text-muted block">Score Salud</span>
            <span className={`font-mono text-xl font-bold ${scoreColor}`}>
              {scoreVal.toFixed(1)} <span className="text-xs text-text-muted font-normal">/ 100</span>
            </span>
          </div>

          <div className="p-3 border border-border-subtle bg-surface/60">
            <span className="font-mono text-[10px] text-text-muted block">Total Dependencias</span>
            <span className="font-mono text-xl font-bold text-text">
              {data?.total_dependencies ?? 0}
            </span>
          </div>

          <div className="p-3 border border-emerald-500/20 bg-emerald-950/20">
            <span className="font-mono text-[10px] text-emerald-400 block">Al Día</span>
            <span className="font-mono text-xl font-bold text-emerald-300">
              {data?.up_to_date_count ?? 0}
            </span>
          </div>

          <div className="p-3 border border-amber-500/20 bg-amber-950/20">
            <span className="font-mono text-[10px] text-amber-400 block">Desactualizadas</span>
            <span className="font-mono text-xl font-bold text-amber-300">
              {data?.outdated_count ?? 0}
            </span>
          </div>

          <div className="p-3 border border-rose-500/20 bg-rose-950/20">
            <span className="font-mono text-[10px] text-rose-400 block">Incompatibles</span>
            <span className="font-mono text-xl font-bold text-rose-300">
              {data?.incompatible_count ?? 0}
            </span>
          </div>
        </div>

        {/* Filter Controls */}
        <div className="flex items-center gap-2 p-3 px-6 border-b border-border-subtle bg-surface/40 overflow-x-auto">
          <span className="font-mono text-xs text-text-muted flex items-center gap-1.5 mr-2">
            <Filter className="size-3.5" /> Filtro:
          </span>
          <button
            type="button"
            onClick={() => setFilterStatus('all')}
            className={`font-mono text-xs px-3 py-1 border transition-colors ${
              filterStatus === 'all'
                ? 'bg-brand text-brand-ink border-brand font-bold'
                : 'border-border-subtle bg-surface text-text-muted hover:text-text'
            }`}
          >
            Todas ({dependencies.length})
          </button>
          <button
            type="button"
            onClick={() => setFilterStatus('incompatible')}
            className={`font-mono text-xs px-3 py-1 border transition-colors ${
              filterStatus === 'incompatible'
                ? 'bg-rose-600 text-white border-rose-500 font-bold'
                : 'border-border-subtle bg-surface text-rose-400 hover:border-rose-500/50'
            }`}
          >
            Incompatibles ({data?.incompatible_count ?? 0})
          </button>
          <button
            type="button"
            onClick={() => setFilterStatus('outdated')}
            className={`font-mono text-xs px-3 py-1 border transition-colors ${
              filterStatus === 'outdated'
                ? 'bg-amber-600 text-white border-amber-500 font-bold'
                : 'border-border-subtle bg-surface text-amber-400 hover:border-amber-500/50'
            }`}
          >
            Desactualizadas ({data?.outdated_count ?? 0})
          </button>
          <button
            type="button"
            onClick={() => setFilterStatus('major')}
            className={`font-mono text-xs px-3 py-1 border transition-colors ${
              filterStatus === 'major'
                ? 'bg-rose-700 text-white border-rose-600 font-bold'
                : 'border-border-subtle bg-surface text-rose-300 hover:border-rose-500/50'
            }`}
          >
            Major Breaking ({data?.major_updates_count ?? 0})
          </button>
          <button
            type="button"
            onClick={() => setFilterStatus('up_to_date')}
            className={`font-mono text-xs px-3 py-1 border transition-colors ${
              filterStatus === 'up_to_date'
                ? 'bg-emerald-600 text-white border-emerald-500 font-bold'
                : 'border-border-subtle bg-surface text-emerald-400 hover:border-emerald-500/50'
            }`}
          >
            Al Día ({data?.up_to_date_count ?? 0})
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto scroll-accent flex-1 flex flex-col gap-3">
          {isLoading ? (
            <div className="text-center py-16 text-text-muted font-mono text-xs flex flex-col items-center gap-3">
              <RefreshCw className="size-6 animate-spin text-brand" />
              <p>Analizando dependencias del repositorio...</p>
            </div>
          ) : filteredDeps.length === 0 ? (
            <div className="text-center py-16 text-text-muted font-mono text-xs flex flex-col items-center gap-2">
              <CheckCircle2 className="size-8 text-emerald-400" />
              <p className="font-bold text-text">No se encontraron dependencias en este filtro.</p>
              <p className="text-text-muted">Todas las dependencias están optimizadas o no coinciden con la condición seleccionada.</p>
            </div>
          ) : (
            filteredDeps.map((dep, idx) => (
              <div
                key={`${dep.package_name}-${idx}`}
                className="border border-border-subtle bg-surface-2/30 hover:border-border-strong p-4 space-y-2.5 transition-colors"
              >
                <div className="flex items-start justify-between gap-3 flex-wrap">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-mono text-sm font-bold text-text">
                      {dep.package_name}
                    </span>
                    <span className="border border-border-subtle bg-surface-2 text-text-muted font-mono text-[10px] uppercase px-2 py-0.5">
                      {dep.ecosystem.toUpperCase()} • {dep.source_file}
                    </span>
                  </div>

                  <div>{getStatusBadge(dep.status)}</div>
                </div>

                {/* Version comparison row */}
                <div className="flex items-center gap-3 flex-wrap font-mono text-xs">
                  <div className="flex items-center gap-1.5">
                    <span className="text-text-muted">Instalada:</span>
                    <code className="bg-bg-deep border border-border-subtle px-2 py-0.5 text-rose-400">
                      {dep.current_version}
                    </code>
                  </div>

                  <span className="text-text-muted">➔</span>

                  <div className="flex items-center gap-1.5">
                    <span className="text-text-muted">Recomendada:</span>
                    <code className="bg-bg-deep border border-border-subtle px-2 py-0.5 text-emerald-400 font-bold">
                      {dep.recommended_version}
                    </code>
                  </div>
                </div>

                {/* Reason */}
                {dep.reason && (
                  <p className="font-sans text-xs text-text-secondary leading-relaxed">
                    <strong className="text-text font-mono">Motivo / Compatibilidad:</strong> {dep.reason}
                  </p>
                )}

                {/* Command row */}
                {dep.upgrade_command && dep.status !== 'up_to_date' && (
                  <div className="flex items-center justify-between p-2 px-3 border border-border-subtle bg-bg-deep gap-3">
                    <code className="font-mono text-xs text-brand truncate">
                      {dep.upgrade_command}
                    </code>

                    <button
                      type="button"
                      onClick={() => handleCopyCommand(dep.upgrade_command, idx)}
                      className="font-mono text-xs px-2.5 py-1 border border-border-subtle bg-surface-2 hover:border-brand/40 text-text-secondary hover:text-text flex items-center gap-1.5 transition-colors flex-shrink-0"
                    >
                      {copiedIndex === idx ? <Check className="size-3 text-emerald-400" /> : <Copy className="size-3" />}
                      <span>{copiedIndex === idx ? 'Copiado' : 'Copiar'}</span>
                    </button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="p-3.5 px-6 border-t border-border-subtle bg-surface-2/40 flex justify-end">
          <button
            type="button"
            onClick={onClose}
            className="font-mono text-xs px-5 py-2 border border-border-subtle bg-surface-2 hover:bg-surface text-text transition-colors"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};
