import React, { useState, useEffect } from 'react';
import { 
  ArrowRight, 
  Play, 
  Terminal, 
  ShieldAlert, 
  Activity, 
  PackageCheck,
  ExternalLink 
} from 'lucide-react';
import { HeroPixelField } from './HeroPixelField';
import { FindingItem } from '../services/api';

interface PraxiaHomeHeroProps {
  onEnterAudit: () => void;
  onEnterExplorer: () => void;
  onEnterFindings: () => void;
  onOpenDependencies: () => void;
  globalScore: number | null;
  lastAnalyzedAt?: string;
  findings: FindingItem[];
  reposCount: number;
  selectedRepoName?: string;
  metrics?: any[];
}

export const OpenNavyHomeHero: React.FC<PraxiaHomeHeroProps> = ({
  onEnterAudit,
  onEnterExplorer,
  onEnterFindings,
  onOpenDependencies,
  globalScore,
  lastAnalyzedAt,
  findings,
  reposCount,
  selectedRepoName,
  metrics,
}) => {
  const [painted, setPainted] = useState(false);
  const [animatedScore, setAnimatedScore] = useState(0);

  // Score count-up animation
  useEffect(() => {
    if (globalScore === null) return;
    const duration = 1000;
    const start = performance.now();
    let frameId = 0;

    const animate = (now: number) => {
      const progress = Math.min((now - start) / duration, 1);
      const easeOut = 1 - Math.pow(1 - progress, 3);
      setAnimatedScore(Math.round((globalScore || 0) * easeOut));
      if (progress < 1) {
        frameId = requestAnimationFrame(animate);
      }
    };
    frameId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frameId);
  }, [globalScore]);

  const criticalCount = findings.filter(
    (f) => f.severidad === 'critical' || f.severidad === 'high'
  ).length;

  return (
    <div className="relative w-full h-full max-h-full overflow-hidden flex flex-col justify-between select-none">
      {/* Background Interactive Pixel Canvas */}
      <HeroPixelField onPainted={() => setPainted(true)} />

      {/* Main Content Area (Centered) */}
      <div className="relative z-10 flex-1 flex flex-col items-center justify-center px-4 sm:px-6 text-center">
        
        {/* Callout Pill (Derived strictly from live data) */}
        <div className="mb-6 pointer-events-auto">
          {criticalCount > 0 ? (
            <button
              onClick={onEnterFindings}
              className="group inline-flex items-center gap-2 border border-brand/40 bg-bg/80 px-3.5 py-1.5 text-left font-mono text-[13px] leading-snug text-brand transition-colors duration-150 ease-out hover:border-brand hover:bg-brand hover:text-bg focus-visible:outline-2 focus-visible:outline-brand"
            >
              <ShieldAlert className="size-4 shrink-0" />
              <span>
                {criticalCount} hallazgos críticos detectados en {selectedRepoName || 'el repositorio'}
              </span>
              <ArrowRight className="size-4 shrink-0 transition-transform duration-150 group-hover:translate-x-0.5" />
            </button>
          ) : (
            <div className="inline-flex items-center gap-2 border border-border-strong bg-bg/80 px-3.5 py-1.5 font-mono text-[13px] leading-snug text-text-secondary">
              <Activity className="size-3.5 text-brand" />
              <span>
                {lastAnalyzedAt
                  ? `Último análisis completado: ${new Date(lastAnalyzedAt).toLocaleDateString()}`
                  : 'Listo para iniciar análisis de arquitectura y AST'}
              </span>
            </div>
          )}
        </div>

        {/* Wordmark Slot: The canvas aligns exactly to this box */}
        <div
          data-hero-wordmark
          className="w-[88%] max-w-4xl h-16 sm:h-20 flex items-center justify-center my-2 pointer-events-none"
        >
          {/* Fallback before canvas paint */}
          {!painted && (
            <span className="font-sans text-4xl sm:text-6xl font-bold tracking-tighter text-brand">
              OPENNAVY
            </span>
          )}
        </div>

        {/* Hero Title & Exact Tagline */}
        <div className="mt-4 max-w-2xl">
          <h1 className="font-mono text-2xl sm:text-3xl font-medium tracking-tight text-text">
            OpenNavy: Sovereign Fleet Navigator
          </h1>
          <p className="mt-3 text-[15px] leading-relaxed text-text-secondary font-mono">
            Autonomous Code Auditing & AI Opportunity Assessment
          </p>
        </div>

        {/* 2 Omarchy Style CTAs (h-10, 40px, rounded-none 0px) */}
        <div className="mt-8 flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full max-w-xs sm:max-w-none justify-center pointer-events-auto">
          <button
            onClick={onEnterAudit}
            className="h-10 px-5 bg-brand text-brand-ink font-mono text-sm font-semibold flex items-center justify-center gap-2 border border-transparent transition-colors duration-150 hover:bg-[#bbdd97] active:scale-[0.96] focus-visible:outline-2 focus-visible:outline-brand"
          >
            <Terminal className="size-4" />
            Iniciar Auditoría
          </button>
          <button
            onClick={onEnterExplorer}
            className="h-10 px-5 border border-border-strong bg-surface text-text font-mono text-sm font-medium flex items-center justify-center gap-2 transition-colors duration-150 hover:bg-surface-2 active:scale-[0.96] focus-visible:outline-2 focus-visible:outline-brand"
          >
            <Play className="size-4 text-brand" />
            DeepCode Explorer
          </button>
        </div>
      </div>

      {/* Compact Metrics Strip (Fixed inside same 100dvh viewport, 0px radius, h-14) */}
      <div className="relative z-10 w-full h-14 bg-surface border-t border-border-subtle ring-elevation flex items-center justify-between px-4 sm:px-8 font-mono text-xs text-text pointer-events-auto">
        {/* Metric 1: Global Score */}
        <div className="flex items-center gap-3">
          <span className="text-text-muted hidden sm:inline">Score Global:</span>
          <span className="text-xl font-bold tracking-tight text-brand tabular-nums font-sans">
            {globalScore !== null ? `${animatedScore}/100` : '--/100'}
          </span>
          <span className="text-[11px] text-text-muted hidden md:inline">
            ({reposCount} repos • {metrics ? metrics.length : 0} métricas)
          </span>
        </div>

        <div className="h-6 w-px bg-border-subtle" />

        {/* Metric 2: Findings Count with direct link */}
        <button
          onClick={onEnterFindings}
          className="flex items-center gap-2 hover:text-brand transition-colors text-left"
        >
          <span className="text-text-muted hidden sm:inline">Hallazgos:</span>
          <span className="text-base font-semibold text-text tabular-nums">
            {findings.length}
          </span>
          {criticalCount > 0 && (
            <span className="px-1.5 py-0.5 bg-destructive/15 text-destructive border border-destructive/30 text-[10px]">
              {criticalCount} críticos
            </span>
          )}
          <ExternalLink className="size-3 text-text-muted hidden sm:inline" />
        </button>

        <div className="h-6 w-px bg-border-subtle" />

        {/* Metric 3: Dependencies Health Modal Trigger */}
        <button
          onClick={onOpenDependencies}
          className="flex items-center gap-2 hover:text-brand transition-colors"
        >
          <PackageCheck className="size-4 text-brand" />
          <span className="hidden sm:inline">Dependencias:</span>
          <span className="text-text-secondary hover:underline underline-offset-2">
            Ver Auditoría
          </span>
        </button>
      </div>
    </div>
  );
};

export const PraxiaHomeHero = OpenNavyHomeHero;
