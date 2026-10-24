import React, { useState } from 'react';
import { CheckCircle2, BookOpen, Wrench, FileCode2 } from 'lucide-react';
import { FindingItem } from '../services/api';

interface FindingsPanelProps {
  findings: FindingItem[];
}

export const FindingsPanel: React.FC<FindingsPanelProps> = ({ findings }) => {
  const [selectedSeverity, setSelectedSeverity] = useState<string>('ALL');

  const filteredFindings = findings.filter((f) => {
    if (selectedSeverity === 'ALL') return true;
    return f.severidad.toUpperCase() === selectedSeverity;
  });

  const criticalCount = findings.filter((f) => f.severidad === 'critical').length;
  const highCount = findings.filter((f) => f.severidad === 'high').length;
  const warnCount = findings.filter((f) => f.severidad === 'warning').length;

  const getSeverityBadgeClass = (sev: string) => {
    switch (sev.toLowerCase()) {
      case 'critical':
        return 'border-red-300 bg-red-50 text-red-700 font-bold';
      case 'high':
        return 'border-amber-300 bg-amber-50 text-amber-800 font-bold';
      case 'warning':
        return 'border-yellow-300 bg-yellow-50 text-yellow-800 font-bold';
      default:
        return 'border-border-subtle bg-surface-2 text-text font-medium';
    }
  };

  return (
    <div className="space-y-6">
      {/* Filters Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-border-subtle">
        <div>
          <h2 className="font-sans text-xl font-bold tracking-tight text-text">
            Hallazgos y Violaciones de Calidad
          </h2>
          <p className="font-mono text-xs text-text-muted mt-0.5">
            Juicios estructurados generados por el LLM contrastados contra la base de conocimiento
          </p>
        </div>

        {/* Severity Filter Pills */}
        <div className="flex items-center gap-2 flex-wrap">
          <button
            type="button"
            onClick={() => setSelectedSeverity('ALL')}
            className={`font-mono text-xs px-3 py-1.5 border transition-all duration-150 cursor-pointer ${
              selectedSeverity === 'ALL'
                ? 'border-[#003893] bg-[#003893] text-white font-semibold shadow-xs'
                : 'border-border-subtle bg-surface text-text hover:text-[#003893] hover:border-[#003893]/40'
            }`}
          >
            Todos ({findings.length})
          </button>
          <button
            type="button"
            onClick={() => setSelectedSeverity('CRITICAL')}
            className={`font-mono text-xs px-3 py-1.5 border transition-all duration-150 cursor-pointer ${
              selectedSeverity === 'CRITICAL'
                ? 'border-red-600 bg-red-600 text-white font-semibold shadow-xs'
                : 'border-border-subtle bg-surface text-red-700 hover:border-red-400'
            }`}
          >
            Críticos ({criticalCount})
          </button>
          <button
            type="button"
            onClick={() => setSelectedSeverity('HIGH')}
            className={`font-mono text-xs px-3 py-1.5 border transition-all duration-150 cursor-pointer ${
              selectedSeverity === 'HIGH'
                ? 'border-amber-600 bg-amber-600 text-white font-semibold shadow-xs'
                : 'border-border-subtle bg-surface text-amber-800 hover:border-amber-400'
            }`}
          >
            Altos ({highCount})
          </button>
          <button
            type="button"
            onClick={() => setSelectedSeverity('WARNING')}
            className={`font-mono text-xs px-3 py-1.5 border transition-all duration-150 cursor-pointer ${
              selectedSeverity === 'WARNING'
                ? 'border-yellow-600 bg-yellow-600 text-white font-semibold shadow-xs'
                : 'border-border-subtle bg-surface text-yellow-800 hover:border-yellow-400'
            }`}
          >
            Advertencias ({warnCount})
          </button>
        </div>
      </div>

      {/* Findings List */}
      {filteredFindings.length === 0 ? (
        <div className="border border-border-subtle bg-surface p-12 text-center flex flex-col items-center justify-center gap-3">
          <CheckCircle2 className="size-10 text-emerald-400" />
          <h3 className="font-sans text-base font-bold text-text">No hay violaciones detectadas</h3>
          <p className="font-mono text-xs text-text-muted max-w-md">
            El código analizado cumple satisfactoriamente con los criterios de calidad y principios evaluados en esta categoría.
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-3.5">
          {filteredFindings.map((f, idx) => (
            <div
              key={f.id || idx}
              className="border border-border-subtle bg-surface/90 hover:border-border-strong p-5 transition-colors duration-150 flex flex-col gap-3"
            >
              <div className="flex items-start justify-between gap-3 flex-wrap">
                <div className="flex items-center gap-2.5 flex-wrap">
                  <span
                    className={`font-mono text-[11px] uppercase tracking-wider font-bold px-2 py-0.5 border ${getSeverityBadgeClass(
                      f.severidad
                    )}`}
                  >
                    {f.severidad}
                  </span>
                  <span className="font-mono text-[11px] px-2 py-0.5 border border-border-subtle bg-surface-2 text-text font-medium">
                    {f.criterio.replace('_', ' ')}
                  </span>
                  <div className="flex items-center gap-1.5 font-mono text-xs text-text break-all">
                    <FileCode2 className="size-4 text-[#003893] flex-shrink-0" />
                    <strong>{f.file_path}</strong>
                    {f.line_number && <span className="text-text-muted">:L{f.line_number}</span>}
                    {f.function_name && <span className="text-[#003893] font-semibold">({f.function_name})</span>}
                  </div>
                </div>

                {f.rag_source && (
                  <div className="flex items-center gap-1.5 font-mono text-[11px] text-[#003893] border border-[#003893]/30 bg-[#003893]/10 px-2.5 py-0.5 flex-shrink-0 font-medium">
                    <BookOpen className="size-3" />
                    <span>Fuente: {f.rag_source}</span>
                  </div>
                )}
              </div>

              {/* Explanation */}
              <p className="font-sans text-sm text-text leading-relaxed">
                {f.explicacion}
              </p>

              {/* Refactoring Suggestion */}
              {f.sugerencia && (
                <div className="border-l-2 border-emerald-600 bg-emerald-50/80 p-3.5 flex items-start gap-3 mt-1">
                  <Wrench className="size-4 text-emerald-700 flex-shrink-0 mt-0.5" />
                  <div className="space-y-1">
                    <span className="font-mono text-[11px] font-bold text-emerald-800 uppercase tracking-wider block">
                      Sugerencia de Refactorización:
                    </span>
                    <p className="font-sans text-xs text-text leading-relaxed">{f.sugerencia}</p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
