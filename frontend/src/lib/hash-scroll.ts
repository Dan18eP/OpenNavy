import type React from 'react'

export function useHashLink(hash: string) {
  return (event: React.MouseEvent) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return
    }
    const target = document.getElementById(hash)
    if (!target) return

    event.preventDefault()
    target.scrollIntoView({
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches
        ? 'auto'
        : 'smooth',
      block: 'start',
    })
    try {
      history.replaceState(null, '', `#${hash}`)
    } catch {
      /* ignore */
    }
  }
}

export function useTopLink() {
  return (event: React.MouseEvent) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return
    }
    event.preventDefault()
    window.scrollTo({
      top: 0,
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches
        ? 'auto'
        : 'smooth',
    })
    try {
      history.replaceState(null, '', '#home')
    } catch {
      /* ignore */
    }
  }
}
