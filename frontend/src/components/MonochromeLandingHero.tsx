import React from 'react';
import { 
  Terminal, 
  Cpu, 
  ArrowRight, 
  Compass
} from 'lucide-react';

interface MonochromeLandingProps {
  onEnterAudit: () => void;
  onEnterAssessment: () => void;
  onEnterDeepCode: () => void;
  reposCount: number;
}

export const MonochromeLandingHero: React.FC<MonochromeLandingProps> = ({
  onEnterAudit,
  onEnterAssessment,
  onEnterDeepCode,
  reposCount
}) => {
  return (
    <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-[#0c100e] text-neutral-100 p-8 md:p-14 mb-10 backdrop-blur-2xl">
      {/* Decorative Noise & Minimalist Lines */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-emerald-500/10 to-transparent rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-20 -left-20 w-80 h-80 bg-gradient-to-tr from-cyan-500/10 to-transparent rounded-full blur-3xl pointer-events-none" />

      {/* Top Meta Line */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8 pb-6 border-b border-white/10">
        <div className="flex items-center gap-3">
          <span className="w-2.5 h-2.5 rounded-full bg-[#003893] animate-pulse" />
          <span className="font-mono text-xs uppercase tracking-widest text-[#003893]">
            OPENNAVY FLEET OS · SOVEREIGN AI & CODE AUDIT
          </span>
        </div>
        <div className="flex items-center gap-4 text-xs font-mono text-neutral-400">
          <span>{reposCount} REPOS CONECTADOS</span>
          <span>•</span>
          <span>OWASP TOP 10 COMPLIANT</span>
        </div>
      </div>

      {/* Hero Headline & Conceptual Art Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
        {/* Left Column (Text & Triggers) */}
        <div className="lg:col-span-7 space-y-6">
          <div className="inline-block px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[11px] font-mono text-neutral-300">
            EXPERIENCIA MONOCROMÁTICA EDITORIAL
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight font-mono text-white leading-tight">
            OPENNAVY <span className="text-[#003893] font-sans font-light">SYSTEM</span>
          </h1>
          <p className="text-sm md:text-base text-neutral-300 max-w-xl leading-relaxed">
            Plataforma autónoma de gobernanza de software, auditoría de antipatrones y evaluación cualitativa con <b>RAG Blindado</b>. Integra la metodología formal de viabilidad de la <b>Sesión 01</b> y el visor dividido <b>DeepCode Explorer</b>.
          </p>

          {/* Action CTAs */}
          <div className="flex flex-wrap gap-3 pt-2">
            <button
              onClick={onEnterAudit}
              className="px-6 py-3 rounded-xl bg-[#3BE6C2] hover:bg-[#34cfae] text-black font-mono font-bold text-xs flex items-center gap-2 transition-all shadow-lg shadow-[#3BE6C2]/10"
            >
              <Terminal className="w-4 h-4" />
              <span>Auditar Repositorio</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={onEnterDeepCode}
              className="px-5 py-3 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-white font-mono text-xs border border-white/10 flex items-center gap-2 transition-all"
            >
              <Cpu className="w-4 h-4 text-[#3BE6C2]" />
              <span>DeepCode Explorer</span>
            </button>

            <button
              onClick={onEnterAssessment}
              className="px-5 py-3 rounded-xl bg-neutral-900/60 hover:bg-neutral-800 text-neutral-300 font-mono text-xs border border-white/10 flex items-center gap-2 transition-all"
            >
              <Compass className="w-4 h-4 text-emerald-400" />
              <span>AI Assessment (Sesión 01)</span>
            </button>
          </div>
        </div>

        {/* Right Column: Monochromatic Technical Showcase (5 cols) */}
        <div className="lg:col-span-5 p-6 rounded-2xl border border-white/10 bg-black/60 relative backdrop-blur-xl">
          <div className="flex items-center justify-between pb-3 mb-4 border-b border-white/10 text-xs font-mono text-neutral-400">
            <span>PIPELINE CAPABILITIES</span>
            <span className="text-[#3BE6C2]">VERIFICADO</span>
          </div>

          <div className="space-y-3 font-mono text-xs">
            <div className="p-3 rounded-xl bg-neutral-950/80 border border-white/5 flex items-start gap-3">
              <span className="w-5 h-5 rounded-md bg-[#3BE6C2]/10 text-[#3BE6C2] flex items-center justify-center text-[10px] flex-shrink-0 mt-0.5">
                01
              </span>
              <div>
                <span className="text-white font-medium block">Auditoría Estructural & Ciclos</span>
                <span className="text-[11px] text-neutral-400">McCabe CC, Halstead MI y grafos DFS de capas limpias.</span>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-neutral-950/80 border border-white/5 flex items-start gap-3">
              <span className="w-5 h-5 rounded-md bg-[#3BE6C2]/10 text-[#3BE6C2] flex items-center justify-center text-[10px] flex-shrink-0 mt-0.5">
                02
              </span>
              <div>
                <span className="text-white font-medium block">AI Opportunity Assessment</span>
                <span className="text-[11px] text-neutral-400">Sesión 01: Perfil de 7 capacidades y veredicto de necesidad de IA.</span>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-neutral-950/80 border border-white/5 flex items-start gap-3">
              <span className="w-5 h-5 rounded-md bg-[#3BE6C2]/10 text-[#3BE6C2] flex items-center justify-center text-[10px] flex-shrink-0 mt-0.5">
                03
              </span>
              <div>
                <span className="text-white font-medium block">DeepCode Explorer (DeepWiki)</span>
                <span className="text-[11px] text-neutral-400">Split-Pane interactivo con citas de código y navegación de árbol.</span>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-neutral-950/80 border border-white/5 flex items-start gap-3">
              <span className="w-5 h-5 rounded-md bg-[#3BE6C2]/10 text-[#3BE6C2] flex items-center justify-center text-[10px] flex-shrink-0 mt-0.5">
                04
              </span>
              <div>
                <span className="text-white font-medium block">Escudo OWASP LLM (Sesión 04)</span>
                <span className="text-[11px] text-neutral-400">SecretMasker activo, anti-prompt injection y flags sanitizados.</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
