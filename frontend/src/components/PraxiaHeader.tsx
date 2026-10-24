import React, { useState, useRef, useEffect } from 'react'
import {
  GithubIcon,
  MenuBarsIcon,
  XIcon,
} from '@/components/icons'
import { OmarchyMarkDrawn } from '@/components/Brand'
import { Button } from '@/components/ui/button'
import { RepoItem } from '@/services/api'
import { cn } from '@/lib/utils'
import { Users, Globe, Linkedin } from 'lucide-react'
import { PRAXIA_TEAM, CreditsModal } from '@/components/CreditsModal'

export type TabType =
  | 'overview'
  | 'audit'
  | 'workspace'
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
  findingsCount,
  knowledgeDocsCount,
  repos,
  selectedRepoId,
  onSelectRepo,
  onStartAudit,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [teamDropdownOpen, setTeamDropdownOpen] = useState(false)
  const [creditsModalOpen, setIsCreditsModalOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

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

  const navLinks: { id: TabType; label: string; badge?: number }[] = [
    { id: 'overview', label: 'Inicio' },
    { id: 'audit', label: 'Auditoría', badge: findingsCount },
    { id: 'workspace', label: 'Trazador & Explorador' },
    { id: 'docs', label: 'Documentación', badge: knowledgeDocsCount },
  ]

  return (
    <header className="pixel-container sticky top-0 z-[100]">
      <div
        className={cn(
          'group/bar border-b border-border-subtle bg-bg/90 backdrop-blur-md transition-colors',
          mobileMenuOpen && 'bg-bg/98 backdrop-blur-xl',
        )}
        style={{
          paddingTop: 'env(safe-area-inset-top)',
        }}
      >
        <div className="mx-auto flex h-14 max-w-7xl items-center gap-3 px-4 sm:px-6 lg:px-8">
          {/* Logo Mark: draws authentic Omarchy geometry */}
          <button
            onClick={() => {
              onSelectTab('overview')
              window.scrollTo({ top: 0, behavior: 'smooth' })
            }}
            aria-label="OpenNavy Home"
            className="mark-draw-trigger relative flex items-center gap-2 focus-visible:outline-2 focus-visible:outline-brand"
          >
            <OmarchyMarkDrawn className="size-[22px] shrink-0 lg:size-[calc(var(--pxc)*2)]" />
            <span className="font-sans text-sm font-semibold tracking-tight text-text hidden sm:inline">
              OPENNAVY
            </span>
          </button>

          {/* Desktop Navigation */}
          <nav
            data-nav-links
            aria-label="Main Navigation"
            className="hidden items-center md:flex ml-2"
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
                    'relative px-3 py-1.5 text-sm whitespace-nowrap transition-colors duration-150 ease-out focus-visible:outline-2 focus-visible:outline-ring',
                    isActive
                      ? 'text-text font-medium bg-surface-2'
                      : 'text-text-secondary hover:bg-surface-2 hover:text-text',
                  )}
                >
                  {link.label}
                  {typeof link.badge === 'number' && link.badge > 0 && (
                    <span className="ml-1.5 px-1 py-0.2 text-[10px] font-mono bg-brand/15 text-brand border border-brand/30">
                      {link.badge}
                    </span>
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
                className="hidden lg:block h-8 max-w-[130px] truncate border border-border-strong bg-surface px-2 font-mono text-xs text-text focus-visible:outline-2 focus-visible:outline-ring"
              >
                {repos.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.name}
                  </option>
                ))}
              </select>
            )}

            {/* Team Profiles Selector */}
            <div className="relative" ref={dropdownRef}>
              <Button
                variant="ghost"
                size="icon"
                aria-label="Equipo de desarrollo de Praxia"
                onClick={() => setTeamDropdownOpen(!teamDropdownOpen)}
                className={cn(
                  "hidden sm:inline-flex h-8 w-8 text-text-secondary hover:text-brand transition-colors",
                  teamDropdownOpen && "bg-surface-2 text-brand"
                )}
                title="Equipo & Desarrolladores"
              >
                <Users className="size-4" />
              </Button>

              {/* Mini Selector Popover */}
              {teamDropdownOpen && (
                <div
                  className="absolute right-0 top-full mt-2 w-72 sm:w-80 border border-border-strong bg-surface p-3 shadow-2xl z-50 text-xs font-mono ring-elevation"
                >
                  <div className="flex items-center justify-between pb-2 border-b border-border-subtle mb-2.5">
                    <div className="flex items-center gap-1.5 text-text font-bold">
                      <Users className="size-3.5 text-brand" />
                      <span>Tripulación OpenNavy (3)</span>
                    </div>
                    <span className="text-[10px] text-text-muted">Perfiles</span>
                  </div>

                  <div className="space-y-2">
                    {PRAXIA_TEAM.map((member, idx) => (
                      <div
                        key={idx}
                        className="p-2 border border-border-subtle/80 bg-surface-2/40 hover:border-brand/40 transition-colors flex items-center justify-between gap-2"
                      >
                        <div className="flex items-center gap-2 min-w-0">
                          <span className="size-6 bg-brand-soft border border-brand/40 text-brand text-[10px] font-bold flex items-center justify-center flex-shrink-0">
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
                          {member.portfolio && (
                            <a
                              href={member.portfolio}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="p-1 border border-border-subtle hover:border-brand hover:text-brand text-text-secondary transition-colors"
                              title={`Portafolio de ${member.name}`}
                            >
                              <Globe className="size-3" />
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
                    className="w-full mt-2.5 py-1.5 border border-brand/40 bg-brand-soft hover:bg-brand text-brand hover:text-brand-ink text-center text-[11px] font-semibold transition-colors block"
                  >
                    Ver Créditos & Portafolios
                  </button>
                </div>
              )}
            </div>

            {/* GitHub Link */}
            <Button
              variant="ghost"
              size="icon"
              aria-label="OpenNavy on GitHub"
              className="hidden sm:inline-flex h-8 w-8 text-text-secondary hover:text-text"
              render={
                <a
                  href="https://github.com/Dan18eP/OpenNavy.git"
                  target="_blank"
                  rel="noopener noreferrer"
                />
              }
            >
              <GithubIcon className="size-5" />
            </Button>

            {/* Mobile Hamburger Toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="flex size-8 items-center justify-center text-text-secondary hover:text-text md:hidden"
              aria-label={mobileMenuOpen ? 'Close Menu' : 'Open Menu'}
            >
              {mobileMenuOpen ? (
                <XIcon className="size-5" />
              ) : (
                <MenuBarsIcon className="size-[22px]" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Menu */}
        {mobileMenuOpen && (
          <div className="border-t border-border-subtle bg-bg/95 px-4 py-4 md:hidden">
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
                      'flex items-center justify-between px-3 py-2 text-left font-mono text-sm',
                      isActive
                        ? 'bg-surface-2 text-brand font-medium'
                        : 'text-text-secondary hover:bg-surface hover:text-text',
                    )}
                  >
                    <span>{link.label}</span>
                    {typeof link.badge === 'number' && link.badge > 0 && (
                      <span className="px-1 py-0.2 text-[10px] font-mono bg-brand/15 text-brand border border-brand/30">
                        {link.badge}
                      </span>
                    )}
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
                className="flex items-center justify-center gap-2 px-3 py-2 border border-border-subtle hover:border-brand/40 bg-surface text-text-secondary hover:text-brand font-mono text-xs transition-colors"
              >
                <Users className="size-3.5" />
                <span>Tripulación & Desarrolladores OpenNavy (3)</span>
              </button>
              <div className="flex items-center justify-between text-xs text-text-muted font-mono pt-1">
                <span>{totalRepos} repos active</span>
                <span>OpenNavy v1.0</span>
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
