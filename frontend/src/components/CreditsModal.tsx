import React from 'react';
import { X, Github, Linkedin, Globe, ShieldCheck } from 'lucide-react';

export interface TeamMember {
  name: string;
  role: string;
  initials: string;
  bio: string;
  github: string;
  linkedin: string;
  portfolio?: string;
}

export const OPENNAVY_TEAM: TeamMember[] = [
  {
    name: 'Daniel Echeverría',
    role: 'Lead Architect & Backend Core',
    initials: 'DE',
    bio: 'Arquitectura de software y gobierno de ADRs. Motor central con Tree-sitter AST, grafo de Tarjan SCC e inferencia local soberana con Google Gemma 4.',
    github: 'https://github.com/Dan18eP',
    linkedin: 'https://www.linkedin.com/in/dechever23/',
  },
  {
    name: 'Dylan Gamero',
    role: 'Real-Time & Systems Engineer',
    initials: 'DG',
    bio: 'Radar de colisión arquitectónica y presencia LAN multijugador con WebSockets. Sincronización del Shared Blueprint y validación de red local.',
    github: 'https://github.com/dypok',
    linkedin: 'https://www.linkedin.com/in/dylan-gamero/',
  },
  {
    name: 'Brandon Carranza',
    role: 'Frontend Engineer & Cockpit Navigator',
    initials: 'BC',
    bio: 'Interfaz de cabina de navegación náutica con React 18, Tailwind y estética pixelada. Visor split-view interactivo sincronizado con waypoints de Gemma 4.',
    github: 'https://github.com/brandoncarranza',
    linkedin: 'https://www.linkedin.com/in/brandon-carranza/',
  },
];

export const PRAXIA_TEAM = OPENNAVY_TEAM;

interface CreditsModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CreditsModal: React.FC<CreditsModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[250] bg-black/60 backdrop-blur-md flex items-center justify-center p-4">
      <div className="w-full max-w-3xl bg-surface border border-border-strong ring-elevation p-6 relative flex flex-col gap-6 max-h-[90vh] overflow-y-auto scroll-accent shadow-2xl">
        {/* Tricolor Header Accent */}
        <div className="absolute top-0 left-0 right-0 h-[3px] flex">
          <div className="w-1/2 bg-[#FCD116]" />
          <div className="w-1/4 bg-[#003893]" />
          <div className="w-1/4 bg-[#CE1126]" />
        </div>

        {/* Header */}
        <div className="flex items-start justify-between border-b border-border-subtle pb-4 pt-1">
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs px-2 py-0.5 border border-brand/40 bg-brand-soft text-brand font-semibold">
                TRIPULACIÓN OPENNAVY
              </span>
              <span className="font-mono text-xs text-text-muted">3 Oficiales</span>
            </div>
            <h2 className="font-sans text-xl font-bold tracking-tight text-text mt-1.5">
              Tripulación & Desarrolladores
            </h2>
            <p className="font-mono text-xs text-text-muted mt-0.5">
              Equipo de ingeniería responsable de la arquitectura, inferencia local con Gemma 4 y cabina náutica de OpenNavy
            </p>
          </div>

          <button
            onClick={onClose}
            className="text-text-muted hover:text-text p-1.5 border border-transparent hover:border-border-subtle transition-colors"
            aria-label="Cerrar modal"
          >
            <X className="size-5" />
          </button>
        </div>

        {/* Team Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {OPENNAVY_TEAM.map((member, idx) => (
            <div
              key={idx}
              className="border border-border-subtle bg-surface-2/60 hover:border-brand/40 p-4 transition-all duration-150 flex flex-col justify-between gap-3 group"
            >
              <div>
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2.5">
                    <div className="size-8 rounded-none border border-brand/50 bg-brand-soft text-brand font-mono font-bold flex items-center justify-center text-xs">
                      {member.initials}
                    </div>
                    <div>
                      <h3 className="font-sans text-sm font-bold text-text group-hover:text-brand transition-colors">
                        {member.name}
                      </h3>
                      <span className="font-mono text-[10px] text-text-secondary block">
                        {member.role}
                      </span>
                    </div>
                  </div>
                </div>

                <p className="font-mono text-xs text-text-muted mt-2.5 leading-relaxed">
                  {member.bio}
                </p>
              </div>

              {/* Action Links */}
              <div className="flex items-center gap-2 pt-3 border-t border-border-subtle/80 flex-wrap">
                {member.linkedin && (
                  <a
                    href={member.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 px-2 py-1 border border-border-subtle bg-surface hover:border-[#0077B5] hover:text-[#0077B5] font-mono text-[10px] text-text-secondary transition-colors"
                  >
                    <Linkedin className="size-3" />
                    <span>LinkedIn</span>
                  </a>
                )}

                {member.github && (
                  <a
                    href={member.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 px-2 py-1 border border-border-subtle bg-surface hover:border-text hover:text-text font-mono text-[10px] text-text-secondary transition-colors"
                  >
                    <Github className="size-3" />
                    <span>GitHub</span>
                  </a>
                )}

                {member.portfolio && (
                  <a
                    href={member.portfolio}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 px-2 py-1 border border-border-subtle bg-surface hover:border-brand hover:text-brand font-mono text-[10px] text-text-secondary transition-colors"
                  >
                    <Globe className="size-3" />
                    <span>Portfolio</span>
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Footer info */}
        <div className="pt-3 border-t border-border-subtle flex flex-col sm:flex-row items-center justify-between text-xs font-mono text-text-muted gap-2">
          <div className="flex items-center gap-1.5">
            <ShieldCheck className="size-4 text-emerald-600" />
            <span>OpenNavy · The Sovereign Fleet Navigator</span>
          </div>
          <span>Licencia MIT · MLH Hacktoberfest 2026</span>
        </div>
      </div>
    </div>
  );
};
