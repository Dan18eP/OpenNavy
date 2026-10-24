import React, { useState } from 'react';
import { Sparkles, BookOpen, FileSpreadsheet, FileText } from 'lucide-react';
import { KnowledgeDocument } from '../services/api';
import { AssessmentDashboardView } from './AssessmentDashboardView';
import { AiMessageRenderer } from './AiMessageRenderer';

interface KnowledgeDocsViewProps {
  documents: KnowledgeDocument[];
}

export const KnowledgeDocsView: React.FC<KnowledgeDocsViewProps> = ({ documents }) => {
  const [subTab, setSubTab] = useState<'docs' | 'assessment'>('docs');
  const [selectedIndex, setSelectedIndex] = useState<number>(0);

  const activeDoc = documents[selectedIndex] || documents[0];

  return (
    <div className="w-full h-full overflow-y-auto scroll-accent p-4 sm:p-6 lg:p-8 space-y-6">
      {/* ── TOP HEADER & SUB-TABS SWITCHER ── */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div>
          <h1 className="font-sans text-2xl font-bold tracking-tight text-text">
            Centro de Documentación & Gobernanza
          </h1>
          <p className="font-mono text-xs text-text-muted mt-1">
            Registros de decisiones arquitectónicas (ADRs vivos) y marco de evaluación de oportunidad IA
          </p>
        </div>

        {/* Sub-tab Switcher */}
        <div className="flex items-center gap-1.5 bg-surface border border-border-subtle p-1 self-start sm:self-auto">
          <button
            type="button"
            onClick={() => setSubTab('docs')}
            className={`font-mono text-xs px-3 py-1.5 flex items-center gap-1.5 transition-all cursor-pointer ${
              subTab === 'docs'
                ? 'bg-[#003893] text-white font-semibold shadow-sm'
                : 'text-text-muted hover:text-text'
            }`}
          >
            <FileText className="size-3.5" />
            <span>Documentos Vivos & ADRs ({documents.length})</span>
          </button>

          <button
            type="button"
            onClick={() => setSubTab('assessment')}
            className={`font-mono text-xs px-3 py-1.5 flex items-center gap-1.5 transition-all cursor-pointer ${
              subTab === 'assessment'
                ? 'bg-[#003893] text-white font-semibold shadow-sm'
                : 'text-text-muted hover:text-text'
            }`}
          >
            <FileSpreadsheet className="size-3.5" />
            <span>Evaluación Oportunidad IA</span>
          </button>
        </div>
      </div>

      {/* ── TAB 1: LIVING DOCUMENTS & ADRS ── */}
      {subTab === 'docs' && (
        documents.length === 0 ? (
          <div className="border border-border-subtle bg-surface p-12 text-center flex flex-col items-center justify-center gap-3">
            <BookOpen className="size-10 text-text-muted" />
            <h3 className="font-sans text-base font-bold text-text">Sin documentación viva generada aún</h3>
            <p className="font-mono text-xs text-text-muted max-w-md">
              Al ejecutar una auditoría sobre el repositorio, el Agente Documentador generará automáticamente ADRs (Architecture Decision Records) y resúmenes estructurados de módulos.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
            {/* Sidebar Doc List */}
            <div className="md:col-span-4 border border-border-subtle bg-surface/90 p-4 space-y-3">
              <div className="flex items-center gap-2 pb-3 border-b border-border-subtle">
                <Sparkles className="size-4 text-brand" />
                <h3 className="font-sans text-sm font-bold text-text tracking-tight">
                  Documentos Vivos ({documents.length})
                </h3>
              </div>

              <div className="flex flex-col gap-1.5 max-h-[calc(100vh-280px)] overflow-y-auto scroll-accent pr-1">
                {documents.map((doc, idx) => {
                  const isSelected = selectedIndex === idx;
                  return (
                    <button
                      key={doc.id || idx}
                      type="button"
                      onClick={() => setSelectedIndex(idx)}
                      className={`w-full text-left p-3 border transition-all duration-150 flex flex-col gap-1.5 cursor-pointer ${
                        isSelected
                          ? 'border-[#003893]/50 bg-[#003893]/10 text-text shadow-sm'
                          : 'border-transparent bg-transparent text-text-muted hover:text-text hover:bg-surface-2 hover:border-border-subtle'
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <span
                          className={`font-mono text-[10px] uppercase font-bold px-1.5 py-0.5 border ${
                            doc.tipo === 'adr'
                              ? 'border-amber-400 bg-amber-50 text-amber-800'
                              : 'border-[#003893]/40 bg-[#003893]/10 text-[#003893]'
                          }`}
                        >
                          {doc.tipo.toUpperCase()}
                        </span>
                        <span className="font-mono text-[10px] text-text-muted">
                          {new Date(doc.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <p className={`font-mono text-xs truncate ${isSelected ? 'font-semibold text-text' : 'text-text-secondary'}`}>
                        {doc.titulo}
                      </p>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Main Document Content */}
            <div className="md:col-span-8 border border-border-subtle bg-surface/90 p-6 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-border-subtle">
                <div>
                  <h2 className="font-sans text-xl font-bold tracking-tight text-text">
                    {activeDoc.titulo}
                  </h2>
                  <span className="font-mono text-xs text-text-muted mt-1 block">
                    {activeDoc.path}
                  </span>
                </div>
                <span className="font-mono text-[11px] uppercase tracking-wider font-semibold px-2.5 py-1 border border-emerald-300 bg-emerald-50 text-emerald-800 flex-shrink-0">
                  Autogenerado por IA
                </span>
              </div>

              <div className="bg-surface p-5 border border-border-subtle overflow-x-auto scroll-accent max-h-[calc(100vh-320px)]">
                <AiMessageRenderer content={activeDoc.contenido} />
              </div>
            </div>
          </div>
        )
      )}

      {/* ── TAB 2: AI CAPABILITY ASSESSMENT DASHBOARD ── */}
      {subTab === 'assessment' && (
        <div className="pt-2">
          <AssessmentDashboardView />
        </div>
      )}
    </div>
  );
};
