import React, { useState, useRef, useEffect } from 'react'
import {
  GithubIcon,
  MenuBarsIcon,
  XIcon,
} from '@/components/icons'
import { Button } from '@/components/ui/button'
import { RepoItem } from '@/services/api'
import { cn } from '@/lib/utils'
import { Users, Globe, Linkedin, Anchor, Radio } from 'lucide-react'
import { OPENNAVY_TEAM, CreditsModal } from '@/components/CreditsModal'
import { useFleetSonar } from '@/hooks/useFleetSonar'

export type TabType =
  | 'overview'
  | 'workspace'
  | 'audit'
  | 'docs'
  | 'credits'
  | 'findings'
  | 'architecture'
  | 'knowledge'
  | 'chat'
  | 'assessment'
  | 'explorer'

interface PraxiaHeaderProps {
  activeTab: TabType
  onSelectTab: (tab: TabType) => void
  systemStatus?: string
  totalRepos: number
  findingsCount: number
  knowledgeDocsCount: number
  onDownloadPdf?: () => void
  isDownloadingPdf?: boolean
  repos: RepoItem[]
  selectedRepoId: string | null
  onSelectRepo: (repoId: string) => void
  onStartAudit?: () => void
}

export const PraxiaHeader: React.FC<PraxiaHeaderProps> = ({
  activeTab,
  onSelectTab,
  totalRepos,
  repos,
  selectedRepoId,
  onSelectRepo,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [teamDropdownOpen, setTeamDropdownOpen] = useState(false)
  const [creditsModalOpen, setIsCreditsModalOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Fleet Sonar Real-time Telemetry (US-08 & US-09 - Dylan Gamero)
  const { connected: sonarConnected, crew: sonarCrew, activeCollisions } = useFleetSonar()

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setTeamDropdownOpen(false)
      }
    }
    if (teamDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [teamDropdownOpen])

  // Only two navigation tabs without badges
  const navLinks: { id: TabType; label: string }[] = [
    { id: 'overview', label: 'Inicio' },
    { id: 'workspace', label: 'Trazador & Explorador' },
  ]

  return (
    <header className="pixel-container sticky top-0 z-[100]">
      {/* MLH Accent Strip (Rojo MLH 50%, Azul Eléctrico 25%, Dorado MLH 25%) */}
      <div className="h-[3px] w-full flex bg-transparent">
        <div className="w-1/2 bg-[#E73427]" title="MLH Red" />
        <div className="w-1/4 bg-[#0084C7]" title="MLH Electric Blue" />
        <div className="w-1/4 bg-[#FFC72C]" title="MLH Gold" />
      </div>

      <div
        className={cn(
          'group/bar border-b border-border-subtle bg-bg/95 backdrop-blur-md transition-colors',
          mobileMenuOpen && 'bg-bg/98 backdrop-blur-xl',
        )}
        style={{
          paddingTop: 'env(safe-area-inset-top)',
        }}
      >
        <div className="mx-auto flex h-14 max-w-7xl items-center gap-3 px-4 sm:px-6 lg:px-8">
          {/* Logo en Navbar con Estética MLH / OpenNavy y Fondo Blanco */}
          <button
            onClick={() => {
              onSelectTab('overview')
              window.scrollTo({ top: 0, behavior: 'smooth' })
            }}
            aria-label="OpenNavy Home"
            className="relative flex items-center gap-2.5 focus-visible:outline-2 focus-visible:outline-[#E73427] cursor-pointer group"
          >
            {/* Isotipo del Barco en Hexágono */}
            <div className="h-9 w-9 bg-white border border-[#192531]/20 p-1 flex items-center justify-center shadow-xs group-hover:border-[#E73427] transition-colors">
              <svg viewBox="0 0 100 100" className="size-full">
                <path d="M 32 14 L 12 26 L 12 74 L 50 96 L 88 74 L 88 26 L 68 14" fill="none" stroke="#CBD5E1" strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M 28 83 L 50 96 L 72 83" fill="none" stroke="#192531" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M 30 36 L 48 50 L 30 64" fill="none" stroke="#FFC72C" strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M 56 24 L 74 64 L 56 64 Z" fill="#0084C7" />
                <line x1="34" y1="74" x2="74" y2="74" stroke="#E73427" strokeWidth="8" strokeLinecap="round" />
              </svg>
            </div>

            {/* Tipografía de Marca limpia sin badges */}
            <div className="flex flex-col text-left">
              <span className="font-mono text-sm font-extrabold tracking-tight text-[#192531]">
                OPEN<span className="text-[#E73427]">NAVY</span>
              </span>
              <span className="text-[10px] font-mono text-[#64748B] -mt-0.5 font-medium">
                The Sovereign Fleet Navigator
              </span>
            </div>
          </button>

          {/* Desktop Navigation: ONLY Inicio and Explorador y copiloto */}
          <nav
            data-nav-links
            aria-label="Main Navigation"
            className="hidden items-center md:flex ml-4 gap-1"
          >
            {navLinks.map((link) => {
              const isActive = activeTab === link.id
              return (
                <button
                  key={link.id}
                  onClick={() => {
                    onSelectTab(link.id)
                    if (link.id === 'overview') {
                      window.scrollTo({ top: 0, behavior: 'smooth' })
                    }
                  }}
                  className={cn(
                    'relative px-3.5 py-1.5 text-xs font-mono tracking-wide transition-all duration-150 focus-visible:outline-2 focus-visible:outline-ring cursor-pointer border',
                    isActive
                      ? 'border-[#E73427] bg-[#E73427]/10 text-[#E73427] font-bold shadow-xs'
                      : 'border-transparent text-text-secondary hover:border-border-subtle hover:bg-surface-2 hover:text-text',
                  )}
                >
                  {link.label}
                  {isActive && (
                    <span className="absolute bottom-0 left-0 right-0 h-[2px] bg-[#E73427]" />
                  )}
                </button>
              )
            })}
          </nav>

          {/* Right Controls */}
          <div className="ml-auto flex items-center gap-2 sm:gap-2.5">
            {/* Repo Selector dropdown if repos exist */}
            {repos && repos.length > 0 && (
              <select
                aria-label="Select active repository"
                value={selectedRepoId || ''}
                onChange={(e) => onSelectRepo(e.target.value)}
                className="hidden lg:block h-8 max-w-[150px] truncate border border-border-strong bg-surface px-2 font-mono text-xs text-text focus-visible:outline-2 focus-visible:outline-ring"
              >
                {repos.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.name}
                  </option>
                ))}
              </select>
            )}

            {/* Fleet Sonar Status Indicator */}
            <button
              onClick={() => onSelectTab('workspace')}
              className={cn(
                "hidden sm:flex items-center gap-1.5 px-2.5 py-1 h-8 border text-xs font-mono transition-colors cursor-pointer",
                activeCollisions.length > 0
                  ? "border-[#E73427] bg-[#E73427]/10 text-[#E73427] animate-pulse font-bold"
                  : sonarConnected
                  ? "border-border-subtle bg-surface hover:border-[#0084C7] text-text"
                  : "border-border-subtle bg-surface text-text-muted"
              )}
              title={
                activeCollisions.length > 0
                  ? "Alerta de colisión arquitectónica activa"
                  : "Fleet Sonar LAN activo"
              }
            >
              <Radio
                className={cn(
                  "size-3.5",
                  activeCollisions.length > 0
                    ? "text-[#E73427] animate-bounce"
                    : sonarConnected
                    ? "text-[#0084C7] animate-pulse"
                    : "text-text-muted"
                )}
              />
              <span className="text-[11px] text-text-muted hidden md:inline">Sonar:</span>
              <span className="text-[11px] font-bold">
                {activeCollisions.length > 0 ? "COLISIÓN" : `${sonarCrew.length} en red`}
              </span>
            </button>

            {/* Team Profiles Selector */}
            <div className="relative" ref={dropdownRef}>
              <Button
                variant="ghost"
                size="icon"
                aria-label="Tripulación de OpenNavy"
                onClick={() => setTeamDropdownOpen(!teamDropdownOpen)}
                className={cn(
                  "hidden sm:inline-flex h-8 w-8 text-text-secondary hover:text-[#E73427] transition-colors border border-transparent hover:border-border-subtle",
                  teamDropdownOpen && "bg-surface-2 text-[#E73427] border-border-strong"
                )}
                title="Tripulación de OpenNavy"
              >
                <Users className="size-4" />
              </Button>

              {/* Team Popover */}
              {teamDropdownOpen && (
                <div
                  className="absolute right-0 top-full mt-2 w-72 sm:w-80 border border-border-strong bg-surface p-3 shadow-2xl z-50 text-xs font-mono ring-elevation"
                >
                  <div className="flex items-center justify-between pb-2 border-b border-border-subtle mb-2.5">
                    <div className="flex items-center gap-1.5 text-text font-bold">
                      <Anchor className="size-3.5 text-[#E73427]" />
                      <span>Tripulación OpenNavy (3)</span>
                    </div>
                    <span className="text-[10px] text-text-muted">Oficiales</span>
                  </div>

                  <div className="space-y-2">
                    {OPENNAVY_TEAM.map((member, idx) => (
                      <div
                        key={idx}
                        className="p-2 border border-border-subtle bg-surface-2/60 hover:border-[#E73427]/40 transition-colors flex items-center justify-between gap-2"
                      >
                        <div className="flex items-center gap-2 min-w-0">
                          <span className="size-6 bg-[#E73427]/10 border border-[#E73427]/40 text-[#E73427] text-[10px] font-bold flex items-center justify-center flex-shrink-0">
                            {member.initials}
                          </span>
                          <div className="truncate">
                            <span className="text-text font-semibold text-xs block truncate">
                              {member.name}
                            </span>
                            <span className="text-text-muted text-[10px] block truncate">
                              {member.role}
                            </span>
                          </div>
                        </div>

                        <div className="flex items-center gap-1 flex-shrink-0">
                          {member.linkedin && (
                            <a
                              href={member.linkedin}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="p-1 border border-border-subtle hover:border-[#0077B5] hover:text-[#0077B5] text-text-secondary transition-colors"
                              title={`LinkedIn de ${member.name}`}
                            >
                              <Linkedin className="size-3" />
                            </a>
                          )}
                          {member.github && (
                            <a
                              href={member.github}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="p-1 border border-border-subtle hover:border-text hover:text-text text-text-secondary transition-colors"
                              title={`GitHub de ${member.name}`}
                            >
                              <GithubIcon className="size-3" />
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>

                  <button
                    onClick={() => {
                      setTeamDropdownOpen(false)
                      setIsCreditsModalOpen(true)
                    }}
                    className="w-full mt-2.5 py-1.5 border border-[#E73427]/40 bg-[#E73427]/10 hover:bg-[#E73427] text-[#E73427] hover:text-white text-center text-[11px] font-semibold transition-colors block cursor-pointer"
                  >
                    Ver Tripulación Completa
                  </button>
                </div>
              )}
            </div>

            {/* GitHub Link */}
            <Button
              variant="ghost"
              size="icon"
              aria-label="OpenNavy on GitHub"
              className="hidden sm:inline-flex h-8 w-8 text-text-secondary hover:text-text border border-transparent hover:border-border-subtle"
              render={
                <a
                  href="https://github.com/Dan18eP/OpenNavy"
                  target="_blank"
                  rel="noopener noreferrer"
                />
              }
            >
              <GithubIcon className="size-4.5" />
            </Button>

            {/* Mobile Hamburger Toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="flex size-8 items-center justify-center text-text-secondary hover:text-text md:hidden border border-border-subtle cursor-pointer"
              aria-label={mobileMenuOpen ? 'Close Menu' : 'Open Menu'}
            >
              {mobileMenuOpen ? (
                <XIcon className="size-4" />
              ) : (
                <MenuBarsIcon className="size-[20px]" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Menu */}
        {mobileMenuOpen && (
          <div className="border-t border-border-subtle bg-bg/98 px-4 py-4 md:hidden">
            <nav className="flex flex-col gap-1.5">
              {navLinks.map((link) => {
                const isActive = activeTab === link.id
                return (
                  <button
                    key={link.id}
                    onClick={() => {
                      onSelectTab(link.id)
                      setMobileMenuOpen(false)
                      if (link.id === 'overview') {
                        window.scrollTo({ top: 0, behavior: 'smooth' })
                      }
                    }}
                    className={cn(
                      'flex items-center justify-between px-3 py-2 text-left font-mono text-xs border',
                      isActive
                        ? 'bg-[#E73427]/10 border-[#E73427] text-[#E73427] font-bold'
                        : 'border-transparent text-text-secondary hover:bg-surface hover:text-text',
                    )}
                  >
                    <span>{link.label}</span>
                  </button>
                )
              })}
            </nav>

            <div className="mt-4 pt-4 border-t border-border-subtle flex flex-col gap-2">
              <button
                onClick={() => {
                  setIsCreditsModalOpen(true)
                  setMobileMenuOpen(false)
                }}
                className="flex items-center justify-center gap-2 px-3 py-2 border border-border-subtle hover:border-[#E73427]/40 bg-surface text-text-secondary hover:text-[#E73427] font-mono text-xs transition-colors"
              >
                <Users className="size-3.5" />
                <span>Tripulación OpenNavy (3 Oficiales)</span>
              </button>
              <div className="flex items-center justify-between text-xs text-text-muted font-mono pt-1">
                <span>{totalRepos} repos activos</span>
                <span>OpenNavy v1.0 · MIT</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Credits & Team Modal */}
      <CreditsModal
        isOpen={creditsModalOpen}
        onClose={() => setIsCreditsModalOpen(false)}
      />
    </header>
  )
}
