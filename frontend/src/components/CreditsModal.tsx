import React from 'react';
import { X, Github, Linkedin, Globe, Code2, ShieldCheck, Heart } from 'lucide-react';

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
    bio: 'Gobernanza arquitectónica, ADRs, parser universal AST Tree-sitter, motor Tarjan SCC e inferencia soberana con Google Gemma 4.',
    github: 'https://github.com/Dan18eP',
    linkedin: 'https://www.linkedin.com/in/dechever23/',
  },
  {
    name: 'Brandon Carranza',
    role: 'Frontend Engineer & Cockpit Navigator',
    initials: 'BC',
    bio: 'Cabina de mando náutica (Nautical Cockpit), visor interactivo split-view de waypoints sincronizado con Gemma 4 y ergonomía de usuario.',
    github: 'https://github.com/Brxynxr',
    linkedin: 'https://www.linkedin.com/in/breynerm/',
  },
  {
    name: 'Dylan Gamero',
    role: 'Real-Time & Systems Engineer',
    initials: 'DG',
    bio: 'Sonar de flota en tiempo real, radar de colisión arquitectónica sobre LAN y sincronización de blueprints entre máquinas.',
    github: 'https://github.com/ddamago0',
    linkedin: 'https://www.linkedin.com/in/daniel-martinez-gonzalez-a891b3405',
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
    <div className="fixed inset-0 z-[250] bg-black/70 backdrop-blur-md flex items-center justify-center p-4">
      <div className="w-full max-w-3xl bg-surface border border-border-strong ring-elevation p-6 relative flex flex-col gap-6 max-h-[90vh] overflow-y-auto scroll-accent shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between border-b border-border-subtle pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs px-2 py-0.5 border border-brand/40 bg-brand-soft text-brand font-semibold">
                EQUIPO OPENNAVY
              </span>
              <span className="font-mono text-xs text-text-muted">3 Integrantes</span>
            </div>
            <h2 className="font-sans text-xl font-bold tracking-tight text-text mt-1.5">
              Tripulación & Desarrolladores
            </h2>
            <p className="font-mono text-xs text-text-muted mt-0.5">
              Equipo de ingeniería responsable del diseño, motor de análisis AST y cabina de navegación de OpenNavy
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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {PRAXIA_TEAM.map((member, idx) => (
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
                      <span className="font-mono text-[11px] text-text-secondary block">
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
                    className="inline-flex items-center gap-1.5 px-2.5 py-1 border border-border-subtle bg-surface hover:border-[#0077B5] hover:text-[#0077B5] font-mono text-[11px] text-text-secondary transition-colors"
                  >
                    <Linkedin className="size-3.5" />
                    <span>LinkedIn</span>
                  </a>
                )}

                {member.github && (
                  <a
                    href={member.github}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 px-2.5 py-1 border border-border-subtle bg-surface hover:border-text hover:text-text font-mono text-[11px] text-text-secondary transition-colors"
                  >
                    <Github className="size-3.5" />
                    <span>GitHub</span>
                  </a>
                )}

                {member.portfolio && (
                  <a
                    href={member.portfolio}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 px-2.5 py-1 border border-border-subtle bg-surface hover:border-brand hover:text-brand font-mono text-[11px] text-text-secondary transition-colors"
                  >
                    <Globe className="size-3.5" />
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
            <ShieldCheck className="size-4 text-emerald-400" />
            <span>Praxia Platform · Open Source Architecture</span>
          </div>
          <span>Licencia MIT · 2026</span>
        </div>
      </div>
    </div>
  );
};
