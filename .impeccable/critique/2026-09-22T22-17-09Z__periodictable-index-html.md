---
target: PeriodicTable/index.html
total_score: 27
p0_count: 0
p1_count: 2
timestamp: 2026-09-22T22-17-09Z
slug: periodictable-index-html
---
Method: dual-agent (A: design review · B: detector + browser)

## Design Health Score
| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | Carousel has no position indicator |
| 2 | Match System / Real World | 3 | "38 listas de propiedades" vague |
| 3 | User Control and Freedom | 3 | Rotating hero card has no pause; #es/#en hash scrolls header away |
| 4 | Consistency and Standards | 2 | EN hero is h2 with inline styles; inline-styled headings in gallery/final |
| 5 | Error Prevention | 3 | href="#" fallback if store URL empty |
| 6 | Recognition Rather Than Recall | 3 | Pro caveats before plans explained |
| 7 | Flexibility and Efficiency | 3 | No carousel affordance on mobile |
| 8 | Aesthetic and Minimalist Design | 2 | 10 identical cards, stats strip, gradient band compete; trust message lost |
| 9 | Error Recovery | 2 | No fallback if store link missing; no device/iOS requirements |
| 10 | Help and Documentation | 3 | No Pro pricing / compatibility FAQ |
| **Total** | | **27/40** | **Acceptable (top of band)** |

## Anti-Patterns Verdict
LLM: reads as AI/template: gradient text (.grad, .feature .sym), hero-metric strip (.stats), 10 identical icon tiles (.tile/.ic), blue→violet SaaS gradients (.band, .plan.pro, glow). Original piece: the decorative 18-column periodic table with featured element in the natural gap.
Detector: CLI 0 findings (can't resolve CSS vars). In-browser: 69 hits (~39 distinct; #en duplicates hidden section): dark-glow ~26, ai-color-palette ~17, icon-tile-stack 10, gpt-thin-border-wide-shadow 4, gradient-text 1, low-contrast 1 (false positive on .plan .tag), cramped-padding 1 (borderline, .eyebrow).

## Priority Issues
- [P1] Positioning buried: trust/data sources section is 6th (~84% down on mobile); remembered line "datos en los que puedes confiar" absent; belief ladder step 2 skipped. Fix: trust line in hero, sources after screenshots, concrete element card with source + "no fiable" marker instead of settings chips. Cmd: clarify / layout.
- [P1] Banned SaaS patterns clash with anti-references: gradient text, stats strip, identical tile grids, gradient band/Pro border, violet glow. Fix: solid colors, fold numbers into copy, features as varied rows paired with screenshots, quiet band. Cmd: distill then bolder.
- [P2] Mobile first screen weak: hash load scrolls header off, eyebrow wraps, ghost link wraps, no real screenshot above the fold, 5px hero symbols. Cmd: adapt.
- [P2] Heading semantics: no h1 in EN view, no text-wrap: balance (orphans), inline styles. Cmd: polish.
- [P2] A11y: gradient text 3.03:1 at blue end on light; auto-rotating hero without pause (WCAG 2.2.2); smooth scrollBy ignores reduced motion; white on .ic 3.32:1. Cmd: harden.

## Persona Red Flags
- Student on phone: generic "en tu bolsillo" headline; ~8 screens to reach why data is reliable; Pro price unknown and "Con Pro" in 4/6 tiles signals paywall; no iOS/device requirements.
- Teacher: provenance and "apta para cualquier edad" near bottom.
- Screen reader/keyboard: EN view lacks h1; carousel ul tabindex=0 without focus style/instructions.

## Minor Observations
ease instead of exponential easing; store hover lift without reduced-motion guard; system font gives no brand voice; og:image relative URL; chips mix units with features; Watch tile uneven in grid.

## Questions to Consider
- If trusted data is the differentiator, why isn't the hero a real element card with its source and uncertainty?
- Does a student need 4 big numbers and 10 cards, or 3 screenshots with one sentence each?
- Why does privacy (belief 3) get the loudest block while reliability (belief 2) gets kelvin/dark-mode chips?
