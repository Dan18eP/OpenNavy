import { t, language } from '@/i18n/site'
import { OmarchyWordmark } from '@/components/Brand'
import { PixelBackdrop } from '@/components/HeroShader'
import {
  CloudflareMark,
  DigitalOceanMark,
  ThirtySevenSignalsMark,
} from '@/components/PartnerLogos'

const columns = [
  {
    title: t('Explore'),
    links: [
      { label: t('News'), href: 'https://omarchy.org/news/' },
      { label: t('Manual'), href: 'https://omarchy.org/manual/' },
      { label: t('Plugins'), href: 'https://plugins.omarchy.org' },
      { label: t('Themes'), href: '#themes' },
    ],
  },
  {
    title: t('Community'),
    links: [
      { label: 'Discord', href: 'https://discord.gg/tXFUdasqhY' },
      { label: t('Meetups'), href: 'https://omarchy.org/meetups/' },
      { label: t('Teams'), href: 'https://omarchy.org/teams/' },
      { label: t('Workstations'), href: 'https://omarchy.org/workstations/' },
      { label: t('Doctrine'), href: 'https://omarchy.org/doctrine/' },
    ],
  },
  {
    title: t('Foundation'),
    links: [
      { label: t('About'), href: 'https://omarchy.org/foundation/' },
      { label: t('Staff'), href: 'https://omarchy.org/staff/' },
      { label: t('Patrons'), href: 'https://omarchy.org/patrons/' },
      { label: t('Sponsorships'), href: 'https://omarchy.org/sponsorships/' },
      { label: 'AIR', href: 'https://omarchy.org/air/' },
    ],
  },
  {
    title: t('Project'),
    links: [
      { label: t('Security'), href: 'https://omarchy.org/security/' },
      { label: 'GitHub', href: 'https://github.com/omacom/omarchy' },
      { label: t('Brand'), href: 'https://omarchy.org/brand/' },
      {
        label: t('Merch'),
        href: 'https://supply.37signals.com/collections/omarchy',
      },
    ],
  },
] as const

const focusRing =
  'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring'

const footerLink = `text-text-secondary underline decoration-transparent underline-offset-4 transition-colors duration-150 ease-out hover:text-brand hover:decoration-current ${focusRing}`

export function SiteFooter({ onHomeClick }: { onHomeClick?: () => void }) {
  return (
    <footer
      className="relative isolate overflow-hidden border-t border-border-subtle"
      style={{
        background: 'var(--t-field-bg)',
        paddingBottom: 'env(safe-area-inset-bottom)',
      }}
    >
      <PixelBackdrop className="footer-rise" />

      <div className="footer-rise relative mx-auto max-w-6xl px-4 py-14 sm:px-6">
        <div className="flex flex-col gap-10 lg:flex-row lg:justify-between">
          <div className="flex w-full shrink-0 flex-col sm:w-max lg:w-96 lg:self-start">
            <a
              href="#home"
              aria-label={t('Omarchy home')}
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
              <OmarchyWordmark className="h-6 w-auto text-brand transition-colors duration-150 ease-out group-hover:text-[color:var(--t-field-hover)]" />
            </a>
            <p
              data-quiet
              className="mt-4 text-sm leading-relaxed text-text-muted [text-wrap:pretty]"
            >
              <span className="block">
                {t('Beautiful, fun & agentic Linux')}{' '}
                <span className="whitespace-nowrap">
                  {t('by')}{' '}
                  <a href="https://dhh.dk" target="_blank" rel="noreferrer" className={footerLink}>
                    DHH
                  </a>
                </span>
              </span>
              <span className="block">
                {t('The malleable OS for the age of agents.')}
              </span>
            </p>

            <div className="mt-4 flex flex-col text-sm leading-relaxed text-text-muted [text-wrap:pretty]">
              <p data-quiet>
                {t('Incubated at')}{' '}
                <a href="https://37signals.com" target="_blank" rel="noreferrer" className={footerLink}>
                  <ThirtySevenSignalsMark className="mr-[3px] inline-block size-4 shrink-0 align-[-0.28em]" />
                  37signals
                </a>
              </p>
              <p data-quiet>
                {t('Hosting by')}{' '}
                <a href="https://cloudflare.com" target="_blank" rel="noreferrer" className={footerLink}>
                  <CloudflareMark className="mr-[5px] inline-block h-3 w-auto shrink-0 align-[-0.15em]" />
                  Cloudflare
                </a>
              </p>
              <p data-quiet>
                {t('Compute by')}{' '}
                <a href="https://www.digitalocean.com" target="_blank" rel="noreferrer" className={footerLink}>
                  <DigitalOceanMark className="mr-[5px] inline-block size-4 shrink-0 align-[-0.2em]" />
                  DigitalOcean
                </a>
              </p>
            </div>
          </div>

          <div className="grid min-w-0 flex-1 grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-4 xl:gap-x-10">
            {columns.map((col) => (
              <nav key={col.title} data-quiet aria-label={col.title}>
                <h2 className="font-sans text-xs tracking-widest text-text-muted uppercase">
                  {col.title}
                </h2>
                <ul className="mt-3.5 flex flex-col gap-2.5">
                  {col.links.map((link) => (
                    <li key={link.label}>
                      <a href={link.href} className={`text-sm ${footerLink}`}>
                        {link.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </nav>
            ))}
          </div>
        </div>

        <div className="mt-12 flex flex-col gap-2 border-t border-border-subtle pt-6 text-[13px] text-text-muted sm:flex-row sm:items-center sm:justify-between">
          <p data-quiet>
            <a href="https://omarchy.org/brand/" target="_blank" rel="noreferrer" className={footerLink}>
              Omarchy™
            </a>
            {t('. All rights reserved.')}
          </p>
          <p data-quiet>
            {t('Partner inquiries:')}{' '}
            <a href="mailto:foundation@omarchy.org" className={footerLink}>
              foundation@omarchy.org
            </a>
          </p>
        </div>
      </div>
    </footer>
  )
}
