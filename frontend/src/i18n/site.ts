export const language = 'en'
export const locale = { name: 'English', domain: 'https://omarchy.org', formatLocale: 'en-US' }
export const contentLocale = 'en'

export function t(english: string): string {
  return english
}

export function formatNumber(val: number, digits = 0) {
  return new Intl.NumberFormat('en-US', {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  }).format(val)
}

export function hasTranslation(_code: string, _path: string): boolean {
  return false
}

export const sortedLocales: Array<[string, { name: string; domain: string }]> = [
  ['en', { name: 'English', domain: 'https://omarchy.org' }],
]
