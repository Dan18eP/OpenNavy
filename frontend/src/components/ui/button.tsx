import React from 'react'
import { cn } from '@/lib/utils'

export type ButtonVariant =
  | 'default'
  | 'outline'
  | 'secondary'
  | 'ghost'
  | 'destructive'
  | 'link'

export type ButtonSize =
  | 'xs'
  | 'sm'
  | 'default'
  | 'lg'
  | 'icon-xs'
  | 'icon-sm'
  | 'icon'
  | 'icon-lg'

const variantStyles: Record<ButtonVariant, string> = {
  default:
    'bg-primary text-primary-foreground hover:bg-[color-mix(in_oklch,var(--color-primary),white_14%)]',
  outline:
    'border border-border-strong bg-surface text-text hover:bg-surface-2 aria-expanded:bg-surface-2',
  secondary:
    'bg-surface-2 text-text hover:bg-[color-mix(in_oklch,var(--color-surface-2),var(--color-text)_8%)] aria-expanded:bg-surface-2',
  ghost: 'text-text hover:bg-surface-2 aria-expanded:bg-surface-2',
  destructive: 'bg-destructive/10 text-destructive hover:bg-destructive/20',
  link: 'text-primary underline-offset-4 hover:underline',
}

const sizeStyles: Record<ButtonSize, string> = {
  xs: "h-8 gap-1.5 px-2.5 text-xs has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2 [&_svg:not([class*='size-'])]:size-4",
  sm: "h-9 gap-1.5 px-3 text-sm has-data-[icon=inline-end]:pr-2.5 has-data-[icon=inline-start]:pl-2.5 [&_svg:not([class*='size-'])]:size-4",
  default:
    "h-10 gap-2 px-4 text-sm has-data-[icon=inline-end]:pr-3.5 has-data-[icon=inline-start]:pl-3.5 [&_svg:not([class*='size-'])]:size-5",
  lg: "h-11 gap-2 px-5 text-[15px] has-data-[icon=inline-end]:pr-4.5 has-data-[icon=inline-start]:pl-4.5 [&_svg:not([class*='size-'])]:size-5",
  'icon-xs': "size-8 [&_svg:not([class*='size-'])]:size-4",
  'icon-sm': "size-9 [&_svg:not([class*='size-'])]:size-4",
  icon: "size-10 [&_svg:not([class*='size-'])]:size-5",
  'icon-lg': "size-11 [&_svg:not([class*='size-'])]:size-5",
}

export function buttonVariants({
  variant = 'default',
  size = 'default',
  className = '',
}: {
  variant?: ButtonVariant
  size?: ButtonSize
  className?: string
} = {}) {
  return cn(
    'group/button inline-flex shrink-0 items-center justify-center rounded-lg border border-transparent bg-clip-padding font-medium whitespace-nowrap outline-none transition-[background-color,border-color,color,transform] duration-150 ease-out select-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-solid focus-visible:outline-ring active:scale-[0.96] disabled:pointer-events-none disabled:opacity-50 aria-invalid:border-destructive [&_svg]:pointer-events-none [&_svg]:shrink-0',
    variantStyles[variant],
    sizeStyles[size],
    className,
  )
}

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  nativeButton?: boolean
  render?: React.ReactElement
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = 'default',
      size = 'default',
      nativeButton = true,
      render,
      children,
      onClick,
      ...props
    },
    ref,
  ) => {
    const combinedClassName = buttonVariants({ variant, size, className })

    if (render && React.isValidElement(render)) {
      const renderProps = (render as any).props || {}
      return React.cloneElement(render as any, {
        className: cn(combinedClassName, renderProps.className),
        onClick: (e: any) => {
          if (onClick) onClick(e)
          if (renderProps.onClick) renderProps.onClick(e)
        },
        children: children ?? renderProps.children,
      })
    }

    return (
      <button
        ref={ref}
        data-slot="button"
        className={combinedClassName}
        onClick={onClick}
        {...props}
      >
        {children}
      </button>
    )
  },
)

Button.displayName = 'Button'
