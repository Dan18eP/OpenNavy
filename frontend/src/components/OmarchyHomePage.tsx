import React, { useEffect, useLayoutEffect, useState } from 'react'
import {
  DownloadIcon,
  PlayIcon,
} from '@/components/icons'
import { PraxiaWordmark, WORDMARK_BANDS } from '@/components/Brand'
import { HeroShader } from '@/components/HeroShader'
import { DottedSurface } from '@/components/ui/dotted-surface'
import { SectionAnchor } from '@/components/SectionHeading'
import { Button } from '@/components/ui/button'

interface OmarchyHomePageProps {
  onStartAudit?: () => void
  onNavigate?: (tab: string) => void
  onOpenDependencies?: () => void
  lastAnalyzed?: string | null
  findingsCount?: number
  score?: number | null
}

export function OmarchyHomePage({
  onStartAudit,
  onNavigate,
  onOpenDependencies,
  findingsCount = 0,
  score,
  lastAnalyzed,
}: OmarchyHomePageProps) {
  const [painted, setPainted] = useState(false)
  const [intro, setIntro] = useState(false)

  useEffect(() => {
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      setPainted(true)
    }
  }, [])

  useLayoutEffect(() => {
    if (painted) document.documentElement.classList.remove('etch-pending')
  }, [painted])

  useEffect(() => {
    if (!sessionStorage.getItem('praxia-intro-seen')) {
      sessionStorage.setItem('praxia-intro-seen', 'true')
      setIntro(true)
    }
  }, [])

  const displayScore = typeof score === 'number' ? `${score}/100` : '—'

  return (
    <div className="w-full h-full flex flex-col justify-between overflow-hidden select-none">
      {/* ------------------------------------------------------------- 1. HERO VIEWPORT */}
      <section
        id="home"
        data-hero-sentinel
        className={
          'pixel-container relative flex-1 flex flex-col justify-between overflow-hidden select-none [-webkit-touch-callout:none] bg-[#090a0f]' +
          (intro ? ' hero-intro' : '')
        }
      >
        {/* Three.js 3D Dotted Surface Background */}
        <DottedSurface className="absolute inset-0 z-0 opacity-80" />

        {/* Hero Pixel Field with Wordmark Laser-Etch & Interactive Cursor Matrix */}
        <HeroShader onPainted={() => setPainted(true)} transparent={true} />

        <div className="pointer-events-none relative flex flex-1 flex-col items-center justify-center px-6 z-10">
          {/* Wordmark Slot */}
          <PraxiaWordmark
            data-hero-wordmark
            className={
              'w-[88%] max-w-4xl text-[color:var(--t-field-lit)] drop-shadow-[0_0_35px_rgba(139,92,246,0.35)]' +
              (painted ? ' invisible' : '')
            }
            background={WORDMARK_BANDS}
          />

          {/* Hero Text and CTAs */}
          <div
            data-hero-quiet
            className="pointer-events-auto mt-6 flex w-full max-w-2xl flex-col items-center text-center"
          >
            <h1
              data-hero-stagger
              style={{ fontFamily: 'var(--font-mono)' }}
              className="text-2xl font-medium tracking-tight text-text [text-wrap:balance] sm:text-3xl"
            >
              <SectionAnchor anchor="home">
                <span className="sr-only">Praxia: </span>
                Autonomous Code Auditing & Architecture Intelligence
              </SectionAnchor>
            </h1>

            <p
              data-hero-stagger
              className="mt-3 text-[14px] leading-relaxed text-text-secondary max-w-xl [text-wrap:balance]"
            >
              Plataforma SAST multi-lenguaje con detección de ciclos acíclicos y evaluación arquitectónica asistida por RAG.
            </p>

            <div
              data-hero-stagger
              data-hero-cta
              className="mt-6 flex w-full max-w-xs flex-col items-stretch gap-3 sm:w-auto sm:max-w-none sm:flex-row"
            >
              <Button
                size="lg"
                className="h-10 pr-4 has-data-[icon=inline-start]:pl-3"
                onClick={onStartAudit}
              >
                <DownloadIcon data-icon="inline-start" />
                Iniciar Auditoría
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="h-10 pr-4 has-data-[icon=inline-start]:pl-3"
                onClick={() => onNavigate?.('workspace')}
              >
                <PlayIcon data-icon="inline-start" className="mr-0.5" />
                Workspace & Copilot
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

