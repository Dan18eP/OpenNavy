import { t } from '@/i18n/site'
import { OmarchyWordmark } from '@/components/Brand'
import { PixelBackdrop } from '@/components/HeroShader'

const columns = [
  {
    title: 'Navegación',
    links: [
      { label: 'Inicio', href: '#home' },
      { label: 'Explorador y copiloto', href: '#workspace' },
    ],
  },
  {
    title: 'Tripulación',
    links: [
      { label: 'Daniel Echeverría', href: 'https://github.com/Dan18eP' },
      { label: 'Dylan Gamero', href: 'https://github.com/dypok' },
      { label: 'Brandon Carranza', href: 'https://github.com/brandoncarranza' },
    ],
  },
  {
    title: 'Comunidad',
    links: [
      { label: 'GitHub OpenNavy', href: 'https://github.com/Dan18eP/OpenNavy' },
      { label: 'Hacktoberfest 2026', href: 'https://hacktoberfest.com' },
    ],
  },
] as const

const focusRing =
  'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring'

const footerLink = `text-text-secondary underline decoration-transparent underline-offset-4 transition-colors duration-150 ease-out hover:text-brand hover:decoration-current ${focusRing}`

export function SiteFooter({ onHomeClick }: { onHomeClick?: () => void }) {
  return (
    <footer
      className="relative isolate overflow-hidden border-t border-border-subtle bg-bg"
      style={{
        paddingBottom: 'env(safe-area-inset-bottom)',
      }}
    >
      <PixelBackdrop className="footer-rise" />

      <div className="footer-rise relative mx-auto max-w-6xl px-4 py-10 sm:px-6">
        <div className="flex flex-col gap-8 lg:flex-row lg:justify-between">
          <div className="flex w-full shrink-0 flex-col sm:w-max lg:w-96 lg:self-start">
            <a
              href="#home"
              aria-label="OpenNavy home"
              onClick={(e) => {
                if (onHomeClick) {
                  e.preventDefault()
                  onHomeClick()
                  window.scrollTo({ top: 0, behavior: 'smooth' })
                }
              }}
              data-quiet
              className={`group block ${focusRing}`}
            >
              <OmarchyWordmark className="h-6 w-auto text-[#003893] transition-colors duration-150 ease-out group-hover:text-[#CE1126]" />
            </a>
            <p
              data-quiet
              className="mt-3 text-sm leading-relaxed text-text-muted [text-wrap:pretty]"
            >
              The Sovereign Fleet Navigator for Open Source Codebases. Desarrollado por Daniel Echeverría, Dylan Gamero y Brandon Carranza bajo Licencia MIT.
            </p>
          </div>

          <div className="grid min-w-0 flex-1 grid-cols-2 gap-x-6 gap-y-8 sm:grid-cols-3 xl:gap-x-10">
            {columns.map((col) => (
              <nav key={col.title} data-quiet aria-label={col.title}>
                <h2 className="font-sans text-xs tracking-widest text-[#003893] uppercase font-bold">
                  {col.title}
                </h2>
                <ul className="mt-3 flex flex-col gap-2">
                  {col.links.map((link) => (
                    <li key={link.label}>
                      <a href={link.href} className={`text-xs ${footerLink}`}>
                        {link.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </nav>
            ))}
          </div>
        </div>

        <div className="mt-8 flex flex-col gap-2 border-t border-border-subtle pt-4 text-xs font-mono text-text-muted sm:flex-row sm:items-center sm:justify-between">
          <p data-quiet>
            OpenNavy™ · Licencia MIT · Major League Hacking 2026
          </p>
          <p data-quiet>
            Google DeepMind Gemma 4 & DigitalOcean Hacktoberfest
          </p>
        </div>
      </div>
    </footer>
  )
}
