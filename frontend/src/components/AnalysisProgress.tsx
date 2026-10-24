import React from 'react';
import { CheckCircle2, Loader2, AlertCircle } from 'lucide-react';

interface ProgressEvent {
  step: string;
  progress: number;
  message: string;
  global_score?: number;
}

interface AnalysisProgressProps {
  currentEvent: ProgressEvent | null;
}

const PIPELINE_STEPS = [
  { id: 'cloning', label: '1. Clonando Repo' },
  { id: 'static_analysis', label: '2. AST & Métricas' },
  { id: 'rag_retrieval', label: '3. Rúbrica RAG' },
  { id: 'rag_evaluation', label: '4. Evaluación SOLID' },
  { id: 'generating_docs', label: '5. Generando ADRs' },
  { id: 'completed', label: '6. Finalizado' },
];

export const AnalysisProgress: React.FC<AnalysisProgressProps> = ({ currentEvent }) => {
  if (!currentEvent) return null;

  const currentStep = currentEvent.step || 'cloning';
  const progressPct = currentEvent.progress || 10;
  const isFailed = currentStep === 'failed';

  return (
    <div className="border border-brand/40 bg-surface/95 p-5 space-y-4 shadow-[0_0_25px_rgba(139,92,246,0.15)]">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {isFailed ? (
            <AlertCircle className="size-5 text-rose-400 flex-shrink-0" />
          ) : currentStep === 'completed' ? (
            <CheckCircle2 className="size-5 text-emerald-400 flex-shrink-0" />
          ) : (
            <Loader2 className="size-5 text-brand animate-spin flex-shrink-0" />
          )}
          <div>
            <h3 className="font-sans text-sm font-bold text-text">
              {isFailed ? 'Error en el Análisis' : currentStep === 'completed' ? 'Auditoría Finalizada' : 'Pipeline de Agentes en Ejecución'}
            </h3>
            <p className="font-mono text-xs text-text-muted mt-0.5">{currentEvent.message}</p>
          </div>
        </div>

        <span className="font-mono text-base font-bold text-brand">
          {progressPct}%
        </span>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-1.5 bg-bg-deep border border-border-subtle overflow-hidden">
        <div
          style={{ width: `${progressPct}%` }}
          className={`h-full transition-all duration-300 ${
            isFailed
              ? 'bg-rose-500'
              : 'bg-brand shadow-[0_0_12px_rgba(139,92,246,0.6)]'
          }`}
        />
      </div>

      {/* Stepper Checklist */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 pt-1">
        {PIPELINE_STEPS.map((st, idx) => {
          const stepOrder = ['cloning', 'static_analysis', 'rag_retrieval', 'rag_evaluation', 'generating_docs', 'completed'];
          const currentIdx = stepOrder.indexOf(currentStep);
          const isDone = currentIdx > idx || currentStep === 'completed';
          const isCurrent = currentIdx === idx && currentStep !== 'completed';

          return (
            <div
              key={st.id}
              className={`flex items-center gap-2 p-2 border font-mono text-[11px] transition-colors ${
                isDone
                  ? 'border-emerald-300 bg-emerald-50 text-emerald-800 font-semibold'
                  : isCurrent
                  ? 'border-[#003893] bg-[#003893] text-white font-bold shadow-sm'
                  : 'border-border-subtle bg-bg-deep/60 text-text-muted'
              }`}
            >
              {isDone ? (
                <CheckCircle2 className="size-3.5 text-emerald-600 flex-shrink-0" />
              ) : isCurrent ? (
                <Loader2 className="size-3.5 text-white animate-spin flex-shrink-0" />
              ) : (
                <span className="size-1.5 rounded-full bg-text-muted flex-shrink-0" />
              )}
              <span className="truncate">{st.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
