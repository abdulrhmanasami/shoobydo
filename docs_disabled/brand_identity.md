# Brand Identity Guidelines

## Colors
- Primary: #1F3A5F (Calm deep blue)
- Secondary: #4A7A8C (Muted teal)
- Accent: #E0A458 (Warm amber)

Usage:
- Backgrounds: Primary or light neutrals
- Text: Primary/dark; links hover use Accent
- Buttons: Primary background, Accent hover

## Typography
- Headings: Inter, Segoe UI, system-ui, sans-serif
- Body: Inter, Segoe UI, system-ui, sans-serif

Examples:
- H1 28–32px, bold; H2 22–24px, semibold; Body 16–18px, regular

## Logo
- Path: `assets/logo.png` (PNG, preferred on light backgrounds)
- Minimum size: 24px height in navigation; 64px+ in hero
- Clear space: keep at least 0.5x logo height around
- Backgrounds: use on white or very light backgrounds; for dark, provide inverted version

How to use in frontend:
- Place a served copy at `apps/frontend/public/assets/logo.png`
- Reference in components as `/assets/logo.png` (Next.js `public` folder)

## Example Header Composition
- Left: Logo (24–28px height)
- Center/Right: Navigation links (12–16px, medium)
- Contrast: Ensure 4.5:1 for text on backgrounds
