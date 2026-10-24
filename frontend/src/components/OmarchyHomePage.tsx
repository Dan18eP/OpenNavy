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
import { Ship, ShieldCheck, Cpu } from 'lucide-react'

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
    if (!sessionStorage.getItem('opennavy-intro-seen')) {
      sessionStorage.setItem('opennavy-intro-seen', 'true')
      setIntro(true)
    }
  }, [])

  return (
    <div className="w-full h-full flex flex-col justify-between overflow-hidden select-none bg-bg">
      {/* ------------------------------------------------------------- 1. HERO VIEWPORT */}
      <section
        id="home"
        data-hero-sentinel
        className={
          'pixel-container relative flex-1 flex flex-col justify-between overflow-hidden select-none [-webkit-touch-callout:none] bg-bg' +
          (intro ? ' hero-intro' : '')
        }
      >
        {/* Three.js 3D Dotted Surface Background with MLH Gradient */}
        <DottedSurface className="absolute inset-0 z-0 opacity-75" />

        {/* Hero Pixel Field with Wordmark Laser-Etch & Interactive Cursor Matrix */}
        <HeroShader onPainted={() => setPainted(true)} transparent={true} />

        <div className="pointer-events-none relative flex flex-1 flex-col items-center justify-center px-6 z-10">
          {/* Wordmark Slot */}
          <PraxiaWordmark
            data-hero-wordmark
            className={
              'w-[88%] max-w-4xl text-[#192531] drop-shadow-[0_4px_24px_rgba(25,37,49,0.12)]' +
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
              className="text-2xl font-bold tracking-tight text-text [text-wrap:balance] sm:text-3xl"
            >
              <SectionAnchor anchor="home">
                <span className="sr-only">OpenNavy: </span>
                The Sovereign Fleet Navigator for Open Source Codebases
              </SectionAnchor>
            </h1>

            <p
              data-hero-stagger
              className="mt-3 text-[14px] leading-relaxed text-text-muted max-w-xl [text-wrap:balance]"
            >
              Carta náutica interactiva y radar arquitectónico multijugador local-first. Explora bases de código complejas, detecta arrecifes de dependencias con Tarjan y traza waypoints con Google Gemma 4.
            </p>

            {/* CTAs */}
            <div
              data-hero-stagger
              data-hero-cta
              className="mt-7 flex w-full max-w-xs flex-col items-stretch gap-3 sm:w-auto sm:max-w-none sm:flex-row"
            >
              <Button
                size="lg"
                className="h-10 px-6 bg-[#E73427] hover:bg-[#D6281B] text-white font-mono text-xs font-semibold shadow-xs cursor-pointer border border-[#E73427]"
                onClick={onStartAudit}
              >
                <DownloadIcon data-icon="inline-start" className="mr-1.5 size-4" />
                Iniciar Auditoría AST
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="h-10 px-6 border-[#192531]/30 bg-white hover:bg-surface-2 text-[#192531] font-mono text-xs font-semibold shadow-xs cursor-pointer hover:border-[#192531]"
                onClick={() => onNavigate?.('workspace')}
              >
                <PlayIcon data-icon="inline-start" className="mr-1.5 size-4 text-[#FFC72C] fill-[#FFC72C]" />
                Explorador y copiloto
              </Button>
            </div>

            {/* Features bar without badges */}
            <div
              data-hero-stagger
              className="mt-8 flex flex-wrap items-center justify-center gap-4 text-xs font-mono text-text-muted"
            >
              <div className="flex items-center gap-1.5">
                <Ship className="size-3.5 text-[#192531]" />
                <span>Carta Náutica (AST + Tarjan)</span>
              </div>
              <span className="text-border-strong">•</span>
              <div className="flex items-center gap-1.5">
                <Cpu className="size-3.5 text-[#FFC72C]" />
                <span>Google Gemma 4 Local</span>
              </div>
              <span className="text-border-strong">•</span>
              <div className="flex items-center gap-1.5">
                <ShieldCheck className="size-3.5 text-[#E73427]" />
                <span>100% Soberano & Sin Nube</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
