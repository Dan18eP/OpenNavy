import React, { useState } from 'react';
import { 
  CheckCircle2, 
  AlertOctagon, 
  Layers, 
  Search, 
  FileCode2, 
  Wrench, 
  BookOpen, 
  Download, 
  Package, 
  ArrowRight,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { FindingItem, ArchitectureData } from '../services/api';

interface UnifiedAuditViewProps {
  findings: FindingItem[];
  architecture: ArchitectureData | null;
  globalScore?: number | null;
  onDownloadPdf?: () => void;
  isDownloadingPdf?: boolean;
  onOpenDependencies?: () => void;
}

type SubTab = 'all' | 'architecture' | 'solid' | 'smells';

export const UnifiedAuditView: React.FC<UnifiedAuditViewProps> = ({
  findings,
  architecture,
  globalScore,
  onDownloadPdf,
  isDownloadingPdf = false,
  onOpenDependencies,
}) => {
  const [activeSubTab, setActiveSubTab] = useState<SubTab>('all');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [expandedFindings, setExpandedFindings] = useState<Record<string, boolean>>({});

  const hasCycles = architecture?.has_circular_dependencies ?? false;
  const cycles = architecture?.ciclos_detectados || [];

  // Metrics counts
  const criticalCount = findings.filter((f) => f.severidad?.toLowerCase() === 'critical').length;
  const highCount = findings.filter((f) => f.severidad?.toLowerCase() === 'high').length;
  const warnCount = findings.filter((f) => f.severidad?.toLowerCase() === 'warning').length;

  const toggleExpand = (id: string) => {
    setExpandedFindings((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  // Filter findings based on subtab, severity, and search
  const filteredFindings = findings.filter((f) => {
    // 1. Subtab filter
    if (activeSubTab === 'solid') {
      const crit = f.criterio?.toLowerCase() || '';
      const exp = f.explicacion?.toLowerCase() || '';
      const isSolid = 
        crit.includes('solid') ||
        crit.includes('srp') ||
        crit.includes('ocp') ||
        crit.includes('lsp') ||
        crit.includes('isp') ||
        crit.includes('dip') ||
        exp.includes('solid') ||
        exp.includes('responsabilidad');
      if (!isSolid) return false;
    } else if (activeSubTab === 'smells') {
      const crit = f.criterio?.toLowerCase() || '';
      const exp = f.explicacion?.toLowerCase() || '';
      const isSmell = 
        crit.includes('smell') ||
        crit.includes('complex') ||
        crit.includes('god') ||
        crit.includes('long') ||
        exp.includes('complejidad') ||
        exp.includes('smell');
      if (!isSmell) return false;
    }

    // 2. Severity filter
    if (selectedSeverity !== 'ALL') {
      if (f.severidad?.toUpperCase() !== selectedSeverity) return false;
    }

    // 3. Search query filter
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchFile = f.file_path?.toLowerCase().includes(q);
      const matchCrit = f.criterio?.toLowerCase().includes(q);
      const matchExp = f.explicacion?.toLowerCase().includes(q);
      const matchFunc = f.function_name?.toLowerCase().includes(q);
      if (!matchFile && !matchCrit && !matchExp && !matchFunc) return false;
    }

    return true;
  });

  const getSeverityBadgeClass = (sev: string = '') => {
    switch (sev.toLowerCase()) {
      case 'critical':
        return 'border-rose-500/40 bg-rose-950/40 text-rose-300';
      case 'high':
        return 'border-amber-500/40 bg-amber-950/40 text-amber-300';
      case 'warning':
        return 'border-yellow-500/40 bg-yellow-950/40 text-yellow-300';
      default:
        return 'border-border-subtle bg-surface-2 text-text-secondary';
    }
  };

  const getScoreBadge = (score?: number | null) => {
    if (typeof score !== 'number') {
      return {
        label: 'Sin evaluar',
        color: 'border-border-subtle bg-surface-2 text-text-muted',
      };
    }
    if (score >= 80) {
      return {
        label: `${score}/100 · Óptimo`,
        color: 'border-emerald-500/40 bg-emerald-950/40 text-emerald-300',
      };
    }
    if (score >= 60) {
      return {
        label: `${score}/100 · Riesgo Moderado`,
        color: 'border-amber-500/40 bg-amber-950/40 text-amber-300',
      };
    }
    return {
      label: `${score}/100 · Crítico`,
      color: 'border-rose-500/40 bg-rose-950/40 text-rose-300',
    };
  };

  const scoreBadge = getScoreBadge(globalScore);

  return (
    <div className="w-full h-full overflow-y-auto scroll-accent p-4 sm:p-6 lg:p-8 space-y-6">
      {/* ── 1. TOP KPI DASHBOARD BAR ── */}
      <div className="border border-border-subtle bg-surface/90 p-5 backdrop-blur-sm shadow-[0_4px_20px_rgba(0,0,0,0.3)]">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-5 pb-5 border-b border-border-subtle">
          <div>
            <div className="flex items-center gap-2.5">
              <span className="font-mono text-xs px-2.5 py-0.5 border border-brand/40 bg-brand-soft text-brand font-semibold">
                AUDITORÍA INTEGRAL
              </span>
              <span className={`font-mono text-xs px-2.5 py-0.5 border font-semibold ${scoreBadge.color}`}>
                Score: {scoreBadge.label}
              </span>
            </div>
            <h1 className="font-sans text-2xl font-bold tracking-tight text-text mt-2">
              Auditoría Estática & Diagnóstico Arquitectónico
            </h1>
            <p className="font-mono text-xs text-text-muted mt-1">
              Violaciones AST, principios de diseño modular y análisis de ciclos acíclicos (Tarjan ADP)
            </p>
          </div>

          {/* Quick Action Buttons */}
          <div className="flex items-center gap-2.5 flex-wrap">
            {onOpenDependencies && (
              <button
                type="button"
                onClick={onOpenDependencies}
                className="inline-flex items-center gap-2 px-3.5 py-2 border border-border-subtle bg-surface text-text hover:border-brand/50 hover:bg-surface-2 font-mono text-xs font-semibold transition-all"
              >
                <Package className="size-4 text-brand" />
                <span>Auditoría de Dependencias</span>
              </button>
            )}

            {onDownloadPdf && (
              <button
                type="button"
                onClick={onDownloadPdf}
                disabled={isDownloadingPdf}
                className="inline-flex items-center gap-2 px-4 py-2 border border-brand bg-brand text-brand-ink font-mono text-xs font-semibold shadow-[0_0_12px_rgba(139,92,246,0.3)] hover:opacity-95 transition-all disabled:opacity-50"
              >
                <Download className="size-4" />
                <span>{isDownloadingPdf ? 'Generando PDF...' : 'Exportar Informe PDF'}</span>
              </button>
            )}
          </div>
        </div>

        {/* KPI Counter Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-5">
          <div className="p-3.5 border border-border-subtle bg-surface-2/60">
            <span className="font-mono text-[11px] text-text-muted block">TOTAL HALLAZGOS</span>
            <span className="font-mono text-2xl font-bold text-text mt-0.5 block">{findings.length}</span>
            <span className="font-mono text-[10px] text-text-muted">Reglas AST evaluadas</span>
          </div>

          <div className="p-3.5 border border-rose-500/20 bg-rose-950/10">
            <span className="font-mono text-[11px] text-rose-300 block">CRÍTICOS</span>
            <span className="font-mono text-2xl font-bold text-rose-300 mt-0.5 block">{criticalCount}</span>
            <span className="font-mono text-[10px] text-rose-400/80">Refactor urgente requerido</span>
          </div>

          <div className="p-3.5 border border-amber-500/20 bg-amber-950/10">
            <span className="font-mono text-[11px] text-amber-300 block">ALTOS / ADVERTENCIAS</span>
            <span className="font-mono text-2xl font-bold text-amber-300 mt-0.5 block">
              {highCount + warnCount}
            </span>
            <span className="font-mono text-[10px] text-amber-400/80">
              {highCount} altos · {warnCount} advertencias
            </span>
          </div>

          <div className={`p-3.5 border ${hasCycles ? 'border-rose-500/30 bg-rose-950/20' : 'border-emerald-500/30 bg-emerald-950/20'}`}>
            <span className={`font-mono text-[11px] block ${hasCycles ? 'text-rose-300' : 'text-emerald-300'}`}>
              ESTADO ARQUITECTURA
            </span>
            <span className={`font-mono text-base font-bold mt-1.5 block truncate ${hasCycles ? 'text-rose-300' : 'text-emerald-300'}`}>
              {hasCycles ? `${cycles.length} Ciclos Tarjan` : 'DAG Acíclico'}
            </span>
            <span className={`font-mono text-[10px] ${hasCycles ? 'text-rose-400/80' : 'text-emerald-400/80'}`}>
              {hasCycles ? 'Violación de Principio ADP' : 'Cumple principio ADP'}
            </span>
          </div>
        </div>
      </div>

      {/* ── 2. UNIFIED SUB-TABS SELECTOR ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-subtle pb-2">
        <div className="flex items-center gap-1.5 overflow-x-auto scroll-accent pb-1 sm:pb-0">
          <button
            type="button"
            onClick={() => setActiveSubTab('all')}
            className={`font-mono text-xs px-3.5 py-2 border transition-all ${
              activeSubTab === 'all'
                ? 'border-brand bg-brand text-brand-ink font-semibold shadow-[0_0_12px_rgba(139,92,246,0.3)]'
                : 'border-border-subtle bg-surface text-text-muted hover:text-text hover:border-brand/40'
            }`}
          >
            Todos los Hallazgos ({findings.length})
          </button>

          <button
            type="button"
            onClick={() => setActiveSubTab('architecture')}
            className={`font-mono text-xs px-3.5 py-2 border transition-all flex items-center gap-1.5 ${
              activeSubTab === 'architecture'
                ? 'border-brand bg-brand text-brand-ink font-semibold shadow-[0_0_12px_rgba(139,92,246,0.3)]'
                : 'border-border-subtle bg-surface text-text-muted hover:text-text hover:border-brand/40'
            }`}
          >
            <Layers className="size-3.5" />
            <span>Arquitectura & Ciclos (ADP)</span>
            {hasCycles && (
              <span className="size-2 rounded-full bg-rose-400 animate-pulse ml-0.5" />
            )}
          </button>

          <button
            type="button"
            onClick={() => setActiveSubTab('solid')}
            className={`font-mono text-xs px-3.5 py-2 border transition-all ${
              activeSubTab === 'solid'
                ? 'border-brand bg-brand text-brand-ink font-semibold shadow-[0_0_12px_rgba(139,92,246,0.3)]'
                : 'border-border-subtle bg-surface text-text-muted hover:text-text hover:border-brand/40'
            }`}
          >
            Principios SOLID
          </button>

          <button
            type="button"
            onClick={() => setActiveSubTab('smells')}
            className={`font-mono text-xs px-3.5 py-2 border transition-all ${
              activeSubTab === 'smells'
                ? 'border-brand bg-brand text-brand-ink font-semibold shadow-[0_0_12px_rgba(139,92,246,0.3)]'
                : 'border-border-subtle bg-surface text-text-muted hover:text-text hover:border-brand/40'
            }`}
          >
            Complejidad & Smells
          </button>
        </div>

        {/* Severity Filter Pills */}
        {activeSubTab !== 'architecture' && (
          <div className="flex items-center gap-2 flex-wrap">
            <button
              type="button"
              onClick={() => setSelectedSeverity('ALL')}
              className={`font-mono text-xs px-2.5 py-1 border transition-all ${
                selectedSeverity === 'ALL'
                  ? 'border-brand/60 bg-brand-soft text-brand-ink font-semibold'
                  : 'border-border-subtle bg-surface text-text-muted hover:text-text'
              }`}
            >
              Cualquier Severidad
            </button>
            <button
              type="button"
              onClick={() => setSelectedSeverity('CRITICAL')}
              className={`font-mono text-xs px-2.5 py-1 border transition-all ${
                selectedSeverity === 'CRITICAL'
                  ? 'border-rose-500 bg-rose-950 text-rose-300 font-semibold'
                  : 'border-border-subtle bg-surface text-text-muted hover:text-rose-300'
              }`}
            >
              Crítico ({criticalCount})
            </button>
            <button
              type="button"
              onClick={() => setSelectedSeverity('HIGH')}
              className={`font-mono text-xs px-2.5 py-1 border transition-all ${
                selectedSeverity === 'HIGH'
                  ? 'border-amber-500 bg-amber-950 text-amber-300 font-semibold'
                  : 'border-border-subtle bg-surface text-text-muted hover:text-amber-300'
              }`}
            >
              Alto ({highCount})
            </button>
            <button
              type="button"
              onClick={() => setSelectedSeverity('WARNING')}
              className={`font-mono text-xs px-2.5 py-1 border transition-all ${
                selectedSeverity === 'WARNING'
                  ? 'border-yellow-500 bg-yellow-950 text-yellow-300 font-semibold'
                  : 'border-border-subtle bg-surface text-text-muted hover:text-yellow-300'
              }`}
            >
              Advertencias ({warnCount})
            </button>
          </div>
        )}
      </div>

      {/* ── 3. ARCHITECTURE VIEW TAB ── */}
      {activeSubTab === 'architecture' && (
        <div className="space-y-6">
          <div className="border border-border-subtle bg-surface/90 p-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border-subtle">
              <div className="flex items-center gap-3">
                <div className="p-2 border border-brand/30 bg-brand-soft text-brand">
                  <Layers className="size-5" />
                </div>
                <div>
                  <h2 className="font-sans text-lg font-bold tracking-tight text-text">
                    Resumen de Arquitectura y Grafo de Módulos
                  </h2>
                  <p className="font-mono text-xs text-text-muted mt-0.5">
                    {architecture?.resumen || 'Análisis de modularidad estructural y dependencias transitivas.'}
                  </p>
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
              <div className="border border-rose-500/30 bg-rose-950/20 p-5 mt-4 space-y-4">
                <div className="flex items-center gap-2 text-rose-300">
                  <AlertOctagon className="size-5 flex-shrink-0 text-rose-400" />
                  <h3 className="font-sans font-bold text-sm text-rose-200">
                    Alerta de Violación ADP: {cycles.length} Ciclo(s) de Importación Detectados por Tarjan
                  </h3>
                </div>
                <p className="font-mono text-xs text-text-secondary leading-relaxed">
                  Las dependencias circulares acoplan fuertemente los módulos, impiden pruebas unitarias aisladas y complican el despliegue independiente. Aplica el principio de inversión de dependencias (DIP) o introduce un mediador.
                </p>

                <div className="space-y-3 pt-2">
                  {cycles.map((cycle, idx) => (
                    <div
                      key={idx}
                      className="border border-rose-500/40 bg-rose-950/30 p-3.5 font-mono text-xs flex flex-wrap items-center gap-2"
                    >
                      <span className="text-rose-400 font-bold">Ciclo #{idx + 1}:</span>
                      {cycle.map((modulePath, mIdx) => (
                        <React.Fragment key={mIdx}>
                          <span className="px-2 py-0.5 bg-rose-900/50 border border-rose-500/30 text-rose-200 font-semibold">
                            {modulePath}
                          </span>
                          {mIdx < cycle.length - 1 && (
                            <ArrowRight className="size-3 text-rose-400" />
                          )}
                        </React.Fragment>
                      ))}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="border border-emerald-500/30 bg-emerald-950/20 p-5 mt-4 flex items-center gap-3">
                <CheckCircle2 className="size-6 text-emerald-400 flex-shrink-0" />
                <div>
                  <h3 className="font-sans font-bold text-sm text-emerald-200">
                    Grafo de Dependencias Limpio y Acíclico
                  </h3>
                  <p className="font-mono text-xs text-emerald-300/80 mt-0.5">
                    No se detectaron ciclos de importación ni violaciones al Principio de Dependencias Acíclicas (ADP). La estructura respeta la dirección de control sin acoplamientos recursivos.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── 4. FINDINGS LIST TAB ── */}
      {activeSubTab !== 'architecture' && (
        <div className="space-y-4">
          {/* Search Box */}
          <div className="relative">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 size-4 text-text-muted" />
            <input
              type="text"
              placeholder="Buscar por archivo, criterio, función o explicación..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-surface border border-border-subtle focus:border-brand text-xs font-mono text-text outline-none transition-colors"
            />
          </div>

          {filteredFindings.length === 0 ? (
            <div className="border border-border-subtle bg-surface p-12 text-center flex flex-col items-center justify-center gap-3">
              <CheckCircle2 className="size-10 text-emerald-400" />
              <h3 className="font-sans text-base font-bold text-text">No se encontraron hallazgos</h3>
              <p className="font-mono text-xs text-text-muted max-w-md">
                No hay hallazgos que coincidan con los filtros seleccionados o el repositorio cumple con las reglas evaluadas.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {filteredFindings.map((finding, idx) => {
                const findingKey = finding.id || `${finding.file_path}-${finding.line_number}-${idx}`;
                const isExpanded = !!expandedFindings[findingKey];

                return (
                  <div
                    key={findingKey}
                    className="border border-border-subtle bg-surface/90 hover:border-border-strong p-4 transition-all duration-150"
                  >
                    {/* Header */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                      <div className="flex items-center gap-2.5 flex-wrap">
                        <span
                          className={`font-mono text-[10px] uppercase font-bold px-2 py-0.5 border ${getSeverityBadgeClass(
                            finding.severidad
                          )}`}
                        >
                          {finding.severidad}
                        </span>
                        <span className="font-mono text-xs font-semibold text-text">
                          {finding.criterio.replace('_', ' ')}
                        </span>
                      </div>

                      <div className="flex items-center gap-2 text-text-muted font-mono text-xs">
                        <FileCode2 className="size-3.5 text-brand" />
                        <span className="text-text-secondary">{finding.file_path}</span>
                        {finding.line_number && (
                          <span className="text-brand">
                            :L{finding.line_number}
                          </span>
                        )}
                        {finding.function_name && (
                          <span className="text-cyan-400 font-mono text-[11px]">
                            ({finding.function_name})
                          </span>
                        )}
                        {finding.rag_source && (
                          <div className="hidden sm:inline-flex items-center gap-1 font-mono text-[10px] text-brand border border-brand/30 bg-brand-soft px-1.5 py-0.5 ml-1">
                            <BookOpen className="size-2.5" />
                            <span>{finding.rag_source}</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Explanation */}
                    <p className="font-sans text-sm text-text-secondary mt-2 leading-relaxed">
                      {finding.explicacion}
                    </p>

                    {/* Expandable Refactor Advice */}
                    {finding.sugerencia && (
                      <div className="mt-3">
                        <button
                          type="button"
                          onClick={() => toggleExpand(findingKey)}
                          className="inline-flex items-center gap-1.5 font-mono text-xs text-brand hover:underline"
                        >
                          {isExpanded ? (
                            <>
                              <ChevronUp className="size-3.5" />
                              <span>Ocultar sugerencia de refactor</span>
                            </>
                          ) : (
                            <>
                              <ChevronDown className="size-3.5" />
                              <span>Ver sugerencia de refactorización</span>
                            </>
                          )}
                        </button>

                        {isExpanded && (
                          <div className="mt-3 pt-3 border-t border-border-subtle font-mono text-xs">
                            <div className="bg-emerald-950/20 p-3 border-l-2 border-emerald-500 text-text-secondary leading-relaxed">
                              <div className="flex items-center gap-1.5 text-emerald-400 font-semibold mb-1">
                                <Wrench className="size-3.5" />
                                <span>Sugerencia de Refactorización:</span>
                              </div>
                              <p className="font-sans text-xs text-text-secondary whitespace-pre-wrap mt-1">
                                {finding.sugerencia}
                              </p>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
