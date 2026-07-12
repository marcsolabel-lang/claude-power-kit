---
name: taste-skill
description: Anti-slop frontend skill for landing pages, portfolios, and redesigns. Enforces brief inference, three dials (variance/motion/density), design system selection, AI-tell avoidance, and a 50-point pre-flight checklist. Not for dashboards or data tables.
---

# tasteskill: Anti-Slop Frontend Skill

> Landing pages, portfolios, and redesigns. Not dashboards, not data tables, not multi-step product UI.
> Every rule below is **contextual**. None of it fires automatically. First read the brief, then pull only what fits.

---

## 0. BRIEF INFERENCE (Read the Room Before Anything Else)

### 0.A Read these signals first
1. **Page kind** — landing (SaaS / consumer / agency / event), portfolio (dev / designer / creative studio), redesign (preserve vs overhaul), editorial / blog.
2. **Vibe words** — "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "editorial", "agency-y", "glassy", "dark tech".
3. **Reference signals** — URLs linked, screenshots pasted, products named, brands competing with.
4. **Audience** — B2B procurement panel vs. design-conscious consumer vs. recruiter scanning a portfolio.
5. **Brand assets that already exist** — logo, color, type, photography. For redesigns, these are starting material.
6. **Quiet constraints** — accessibility-first, public-sector, regulated, trust-first commerce, kids. These OVERRIDE aesthetic preference.

### 0.B Output a one-line "Design Read" before generating
**"Reading this as: \<page kind> for \<audience>, with a \<vibe> language, leaning toward \<design system or aesthetic family>."**

Examples:
- *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion."*
- *"Reading this as: solo designer portfolio for hiring managers, with an editorial / kinetic-type language, leaning toward native CSS + scroll-driven animation + custom typography."*

### 0.C If the brief is ambiguous, ask ONE question only
Never a multi-question dump. Only when the design read genuinely diverges.

### 0.D Anti-Default Discipline
Do NOT default to: AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism, infinite-loop micro-animations, Inter + slate-900.

---

## 1. THE THREE DIALS

After the design read, set three dials. Every layout, motion, and density decision is gated by these.

- **`DESIGN_VARIANCE: 8`** — 1 = Perfect Symmetry, 10 = Artsy Chaos
- **`MOTION_INTENSITY: 6`** — 1 = Static, 10 = Cinematic / Physics
- **`VISUAL_DENSITY: 4`** — 1 = Art Gallery / Airy, 10 = Cockpit / Packed Data

**Baseline:** `8 / 6 / 4`. Overrides happen conversationally.

### 1.A Dial Inference
| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| "redesign - preserve" | match existing | +1 | match existing |
| "redesign - overhaul" | +2 | +2 | match existing |

### 1.B Use-Case Presets
| Use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Redesign - preserve | match | match+1 | match |
| Redesign - overhaul | +2 | +2 | match |

---

## 2. BRIEF → DESIGN SYSTEM MAP

### 2.A When to use an official design system
| Brief reads as… | Reach for |
|---|---|
| Microsoft / enterprise SaaS | `@fluentui/react-components` |
| Google-ish / Material | `@material/web` + Material 3 tokens |
| IBM B2B / analytics | `@carbon/react` + `@carbon/styles` |
| Shopify app surfaces | Polaris React |
| Atlassian / Jira-style | `@atlaskit/*` |
| GitHub devtool | `@primer/css` or `@primer/react-brand` |
| UK public-sector | `govuk-frontend` |
| US public-sector | `uswds` |
| Fast agency MVP | Bootstrap 5.3 |
| Modern accessible React | `@radix-ui/themes` |
| Modern SaaS own components | shadcn/ui |
| Tailwind modern SaaS / AI | Tailwind v4 utilities + `dark:` variant |

**One system per project.** Do not mix.

### 2.B Aesthetic-only briefs (no official package)
| Aesthetic | Honest implementation |
|---|---|
| Glassmorphism | `backdrop-filter`, layered borders, solid-fill fallback |
| Bento (Apple-style) | CSS Grid with mixed cell sizes |
| Brutalism | Native CSS, monospace, raw borders |
| Editorial / magazine | Serif type, asymmetric grid, whitespace |
| Dark tech / hacker | Mono + neon accent |
| Aurora / mesh gradients | SVG or layered radial gradients |
| Kinetic typography | Native CSS animations, GSAP |
| **Apple Liquid Glass** | Web approximation only — `backdrop-filter` + borders. Label as approximation. |

---

## 3. DEFAULT ARCHITECTURE

### 3.A Stack
- **Framework:** React / Next.js. Default to Server Components.
- **Styling:** Tailwind v4. For v4: use `@tailwindcss/postcss`, NOT `tailwindcss` in postcss.
- **Animation:** Motion (`import { motion } from "motion/react"`). `framer-motion` is legacy alias.
- **Fonts:** `next/font` or `@font-face + font-display: swap`. Never `<link>` to Google Fonts.

### 3.B State
- Local `useState` / `useReducer` for isolated UI.
- **NEVER** use `useState` for continuous values (mouse position, scroll progress). Use `useMotionValue` / `useTransform` / `useScroll`.

### 3.C Icons
- **Allowed:** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`
- **Discouraged:** `lucide-react` (only on explicit request)
- **NEVER** hand-roll SVG icons. One family per project.

### 3.D Emoji Policy
Discouraged by default. Replace with icon-library glyphs.

### 3.E Responsiveness
- Breakpoints: `sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`
- Contain layouts: `max-w-[1400px] mx-auto` or `max-w-7xl`
- **NEVER `h-screen`** for hero. ALWAYS `min-h-[100dvh]`
- Grid over flex-math for 2D layouts

---

## 4. DESIGN ENGINEERING DIRECTIVES

### 4.1 Typography
- Display: `text-4xl md:text-6xl tracking-tighter leading-none`
- Body: `text-base text-gray-600 leading-relaxed max-w-[65ch]`
- **Discouraged default:** Inter. Prefer Geist, Outfit, Cabinet Grotesk, Satoshi.
- **SERIF DISCIPLINE:** Serif is VERY DISCOURAGED as default. Only use when brief names a serif font OR aesthetic is genuinely editorial/luxury/publication. **BANNED defaults:** `Fraunces`, `Instrument_Serif`.
- **Emphasis:** use italic/bold of the SAME font, never inject a different family for emphasis.
- **Italic descender clearance:** when italic display type has `y g j p q`, use `leading-[1.1]` min + `pb-1` reserve.

### 4.2 Color
- Max 1 accent color. Saturation < 80%.
- **LILA RULE:** No AI Purple / Blue glow as default. Use neutral bases (Zinc/Slate/Stone) + high-contrast singular accents.
- **COLOR CONSISTENCY LOCK:** Once accent chosen, used on WHOLE page. Never switch mid-page.
- **PREMIUM-CONSUMER PALETTE BAN:** Banned backgrounds: `#f5f1ea`, `#faf7f1`, etc (warm paper/cream). Banned accents: `#b08947`, `#b6553a`, etc (brass/clay/oxblood). Alternatives: Cold Luxury, Forest, Black and Tan, Cobalt+Cream, Terracotta+Slate.

### 4.3 Layout
- **ANTI-CENTER BIAS:** Centered hero avoided when `DESIGN_VARIANCE > 4`. Force split-screen, left-aligned, asymmetric.
- 3-column equal feature cards: BANNED. Use 2-column zig-zag, asymmetric grid, or scroll alternative.

### 4.4 Cards & Shadows
- Cards ONLY when elevation communicates real hierarchy.
- Shadow: tint to background hue. No pure-black shadows.
- **SHAPE CONSISTENCY LOCK:** Pick ONE corner-radius scale. Stick to it.

### 4.5 Interactive States (always implement full cycle)
- Loading, Empty, Error states required
- On `:active`: `-translate-y-[1px]` or `scale-[0.98]`
- **BUTTON CONTRAST CHECK:** Every CTA text readable against background. WCAG AA 4.5:1.
- **CTA BUTTON WRAP BAN:** Button text MUST fit on one line at desktop. 3 words max for primary CTAs.
- **NO DUPLICATE CTA INTENT:** One label per intent per page.
- **FORM CONTRAST CHECK:** Inputs, placeholders, focus rings, labels all pass WCAG AA.

### 4.6 Forms
- Label ABOVE input. Error BELOW. No placeholder-as-label. Ever.

### 4.7 Layout Discipline (Hard Rules)
- **Hero fits viewport:** Headline max 2 lines desktop, subtext max 20 words AND 4 lines, CTAs visible without scroll.
- **Hero top padding cap:** max `pt-24` at desktop.
- **Hero stack discipline:** max 4 text elements (eyebrow OR brand strip, headline, subtext, CTAs). No tiny taglines below CTAs. No trust micro-strips in hero.
- **"Used by / Trusted by" logo wall:** UNDER the hero, never inside it.
- **Nav on ONE line** at desktop. Height max 80px.
- **Bento grids:** Exact cell count (N items = N cells, no empty cells). At least 2-3 cells with real visual variation.
- **Section-Layout-Repetition Ban:** Each layout family max once per page. Min 4 different families across 8 sections.
- **ZIGZAG ALTERNATION CAP:** Max 2 consecutive image+text-split sections. 3rd is a Pre-Flight Fail.
- **EYEBROW RESTRAINT:** Max 1 eyebrow per 3 sections. Count `uppercase tracking` instances — must be ≤ ceil(sectionCount / 3).
- **SPLIT-HEADER BAN:** No "left big headline + right small explainer paragraph" as default section header.
- **Mobile collapse must be explicit per section.**

### 4.8 Image & Visual Assets
Priority order:
1. Image-gen tool (if available in environment)
2. `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}`
3. Tell the user explicitly — leave labeled placeholder slots

**Banned:** div-based fake screenshots. Hand-rolled decorative SVGs. Text-only minimalism.

For logo walls: use Simple Icons (`https://cdn.simpleicons.org/{slug}/ffffff`) or devicon. **LOGO-ONLY rule:** no category labels below logos.

### 4.9 Content Density
- Default per section: short headline (≤8 words) + subparagraph (≤25 words) + one asset OR CTA.
- No data-dump sections. Lists > 5 items need a better component (2-col split, card grid, tabs, accordion, carousel, marquee).
- **Spec sheets:** BANNED as default row+hairline tables. Use 2-col card grid, scroll-snap pills, or grouped chunks.
- **COPY SELF-AUDIT:** Re-read every visible string. Flag: grammatically broken, unclear referents, AI hallucination, LLM-trying-to-sound-thoughtful. Rewrite every flagged string.
- **Fake-precise numbers banned** unless from real data or explicitly labeled mock.

### 4.10 Quotes
- Max 3 lines. Attribution: name + role + company. Typographic quotes (" ") or none.

### 4.11 Page Theme Lock
**ONE theme.** Sections do not invert. If dark mode: ALL sections dark. Light-mode section sandwiched in dark page = broken.

---

## 5. CONTEXT-AWARE PROACTIVITY (tools, not defaults)

- **Liquid Glass / Glassmorphism:** premium consumer, Apple-adjacent, luxury. NOT dashboards/public-sector.
- **Magnetic Micro-physics:** `MOTION_INTENSITY > 5` + premium/playful. Use `useMotionValue` / `useTransform` ONLY.
- **Perpetual Micro-Interactions:** `MOTION_INTENSITY > 5` + section benefits from motion. Spring physics: `{ type: "spring", stiffness: 100, damping: 20 }`.
- **"Motion claimed, motion shown."** If `MOTION_INTENSITY > 4`, page must actually move.
- **MOTION MUST BE MOTIVATED:** Before adding animation, answer "what does this communicate?" Valid: hierarchy, storytelling, feedback, state transition. Invalid: "it looks cool."
- **MARQUEE MAX ONE PER PAGE.**

### 5.A Sticky-Stack Canonical Skeleton
```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div key={i} className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center">
          {card}
        </div>
      ))}
    </div>
  );
}
```

### 5.B Horizontal-Pan Canonical Skeleton
```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",
          end: () => `+=${distance}`,
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

### 5.C Scroll-Reveal Stagger (lighter alternative to GSAP)
```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

### 5.D Forbidden Animation Patterns
- **`window.addEventListener("scroll", ...)`** — BANNED. Use `useScroll()`, ScrollTrigger, IntersectionObserver, or CSS scroll-driven animations.
- Custom scroll progress with `window.scrollY` in React state — BANNED.
- `requestAnimationFrame` loops touching React state — BANNED.
- NEVER mix GSAP / Three.js with Motion in the same component tree.

---

## 6. PERFORMANCE & ACCESSIBILITY

### 6.A Hardware Acceleration
- Animate ONLY `transform` and `opacity`.
- `will-change: transform` sparingly.

### 6.B Reduced Motion (mandatory)
- `MOTION_INTENSITY > 3` MUST honor `prefers-reduced-motion`.
- In Motion: `useReducedMotion()` → degrade to static.
- Infinite loops, parallax, scroll-hijack, magnetic physics MUST collapse under reduced motion.

### 6.C Dark Mode
- Design for BOTH modes from the start.
- Use Tailwind `dark:` OR CSS variables. Pick one per project.
- `prefers-color-scheme` respected by default.

### 6.D Core Web Vitals
- LCP < 2.5s, INP < 200ms, CLS < 0.1.
- Hero image: `next/image priority` or preloaded.

### 6.E DOM Cost
- Grain/noise filters: ONLY on fixed `pointer-events-none` pseudo-elements.
- Lazy-load anything not above-the-fold.

### 6.F Z-Index Restraint
Never `z-50` or `z-10` arbitrarily. Document the z-index scale in a constants file.

---

## 7. DIAL DEFINITIONS

### DESIGN_VARIANCE
- **1-3:** Symmetrical 12-col grid, equal paddings, centered.
- **4-7:** Overlaps, varied aspect ratios, left-aligned headers over centered data.
- **8-10:** Masonry, fractional grid units (`2fr 1fr 1fr`), massive empty zones (`padding-left: 20vw`).
- **Mobile override:** High-variance layouts MUST collapse to single-column `< 768px`.

### MOTION_INTENSITY
- **1-3:** No animations. CSS `:hover` / `:active` only.
- **4-7:** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. Load-in cascades.
- **8-10:** Complex scroll-triggered reveals, parallax, GSAP ScrollTrigger. **NEVER `window.addEventListener('scroll')`.**

### VISUAL_DENSITY
- **1-3:** Huge section gaps (`py-32` to `py-48`). Art gallery.
- **4-7:** Standard spacing (`py-16` to `py-24`).
- **8-10:** Tight paddings. 1px separators. `font-mono` for all numbers.

---

## 8. DARK MODE PROTOCOL

- Token strategy: Tailwind `dark:` variant OR CSS variables (`--surface`, `--text-primary`). Pick one.
- WCAG AA minimum for body text; AAA target for hero copy.
- No pure `#000000` or `#ffffff`. Use off-black and off-white.
- Test in both modes before finishing.

---

## 9. AI TELLS (Forbidden Patterns)

### 9.A Visual
- NO neon/outer glows by default.
- NO pure black (`#000000`).
- NO oversaturated accents.
- NO excessive gradient text on large headers.
- NO custom mouse cursors.

### 9.B Typography
- AVOID Inter as default.
- NO oversized H1s for raw scale — use weight + color for hierarchy.

### 9.C Layout
- NO 3-column equal feature cards.
- Mathematically perfect padding/margins. No floating elements with awkward gaps.

### 9.D Content ("Jane Doe" Effect)
- NO generic names (John Doe, Sarah Chan). Use creative, realistic, locale-appropriate names.
- NO generic avatars. Use believable photo placeholders.
- NO fake-perfect numbers (99.99%, 50%, 1234567). Use organic data (47.2%).
- NO startup-slop brand names (Acme, Nexus, SmartFlow). Invent contextual, premium names.
- NO filler verbs: "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize".

### 9.E External Resources
- NO hand-rolled SVG icons. Use Phosphor/HugeIcons/Radix/Tabler.
- NO div-based fake screenshots.
- NO broken Unsplash links. Use `picsum.photos/seed/{descriptive}/{w}/{h}`.
- shadcn/ui: NEVER in default state. Always customize.

### 9.F Production-Test Tells (hard bans)
- NO version labels in hero (V0.6, BETA, ALPHA, EARLY ACCESS).
- NO "Brand · No. 01"-style sub-eyebrows.
- NO section-number eyebrows (00 / INDEX, 001 · Capabilities).
- NO `01 / 4`-style pagination on tiles.
- Middle-dot (`·`) max 1 per line. Not as default separator for everything.
- NO decorative colored status dots on every list/nav/badge.
- NO decoration text strip at hero bottom (BRAND. MOTION. SPATIAL.).
- NO floating top-right sub-text in section headings.
- NO `border-t` + `border-b` on every row of long lists.
- NO locale/city-name/time/weather strips (for 99% of briefs).
- NO scroll cues (↓ scroll, Scroll to explore).
- NO generic step labels (Stage 1, Step 1, Phase 01). Use verb-noun directly.
- NO pills/labels/tags overlaid on images.
- NO photo-credit captions as decoration.
- NO version footers on marketing pages.
- NO "Quietly in use at" / "Quietly trusted by" headers.
- NO scoring/progress bars with filled background tracks.

### 9.G EM-DASH BAN (the single most-violated Tell)

**Em-dash (`—`) is COMPLETELY banned.** Zero em-dashes anywhere.

- Banned in headlines. Use period or comma.
- Banned in eyebrows / labels / pills / button text / captions.
- Banned in body copy. Restructure: two sentences, comma, parentheses, colon.
- Banned in quote attribution. Use hyphen with spaces (` - `) or line break.
- En-dash (`–`) as separator also banned. Date ranges: hyphen.

**The ONLY permitted dash:** regular hyphen `-`.

If output contains a single `—` or `–`, the output fails Pre-Flight and must be rewritten.

---

## 10. REFERENCE VOCABULARY

### Hero Paradigms
- Asymmetric Split Hero, Editorial Manifesto Hero, Video/Media Mask Hero
- Kinetic-Type Hero, Curtain-Reveal Hero, Scroll-Pinned Hero

### Navigation
- Mac OS Dock Magnification, Magnetic Button, Gooey Menu
- Dynamic Island, Contextual Radial Menu, Floating Speed Dial, Mega Menu Reveal

### Layout & Grids
- Bento Grid, Masonry Layout, Chroma Grid, Split-Screen Scroll, Sticky-Stack Sections

### Cards & Containers
- Parallax Tilt Card, Spotlight Border Card, Glassmorphism Panel
- Holographic Foil Card, Tinder Swipe Stack, Morphing Modal

### Scroll Animations
- Sticky Scroll Stack, Horizontal Scroll Hijack, Locomotive Sequence
- Zoom Parallax, Scroll Progress Path, Liquid Swipe Transition

### Gallery & Media
- Dome Gallery, Coverflow Carousel, Drag-to-Pan Grid
- Accordion Image Slider, Hover Image Trail, Glitch Effect Image

### Typography & Text
- Kinetic Marquee, Text Mask Reveal, Text Scramble Effect
- Circular Text Path, Gradient Stroke Animation, Kinetic Typography Grid

### Micro-Interactions
- Particle Explosion Button, Liquid Pull-to-Refresh, Skeleton Shimmer
- Directional Hover-Aware Button, Ripple Click Effect, Animated SVG Line Drawing
- Mesh Gradient Background, Lens Blur Depth

### Animation Library Choice
- **Motion (`motion/react`)** — default for UI / Bento / state-change
- **GSAP + ScrollTrigger** — full-page scrolltelling and scroll hijacks (isolated leaf components)
- **Three.js / WebGL** — canvas backgrounds, 3D scenes (isolated)
- **NEVER mix GSAP / Three.js with Motion in the same component tree.**

---

## 11. REDESIGN PROTOCOL

### 11.A Detect the Mode
- **Greenfield** — no existing site or full overhaul approved.
- **Redesign - Preserve** — modernise without breaking the brand.
- **Redesign - Overhaul** — new visual language, preserve content and IA.

If ambiguous, ask once: *"Should this redesign preserve the existing brand, or are we starting visually from scratch?"*

### 11.B Audit Before Touching
Document: brand tokens, IA, content blocks, patterns to preserve, patterns to retire, dial reading of existing site, SEO baseline.

### 11.C Preservation Rules
- Do NOT change IA unless asked. Keep page slugs, anchor IDs, nav labels.
- Extract brand colors before applying Section 4.2.
- Preserve copy voice unless asked for rewrite.
- Honor existing accessibility wins.
- Respect existing analytics events.

### 11.D Modernisation Levers (priority order)
1. Typography refresh
2. Spacing & rhythm
3. Color recalibration
4. Motion layer
5. Hero & key-section recomposition
6. Full block replacement (only if unsalvageable)

### 11.F What Never Changes Without Explicit Approval
URL slugs, primary nav labels, form field names, brand logo, legal/consent copy.

---

## 14. FINAL PRE-FLIGHT CHECK

**THIS IS NOT OPTIONAL. Run every box. Fail = not done.**

- [ ] Brief inference declared (Section 0.B one-liner)?
- [ ] Dial values explicit and reasoned from the brief?
- [ ] Design system chosen or aesthetic labeled honestly?
- [ ] Redesign mode detected and audit performed (if applicable)?
- [ ] **ZERO em-dashes (`—`) anywhere on the page.** (non-negotiable)
- [ ] Page Theme Lock: ONE theme for the whole page?
- [ ] Color Consistency Lock: one accent across all sections?
- [ ] Shape Consistency Lock: one corner-radius system?
- [ ] Button Contrast Check: every CTA text WCAG AA 4.5:1?
- [ ] CTA Button Wrap: no label wraps to 2+ lines at desktop?
- [ ] Form Contrast Check: inputs, placeholders, focus rings, labels pass WCAG AA?
- [ ] Serif discipline: NOT Fraunces or Instrument_Serif (without justification)?
- [ ] Premium-consumer palette check: NOT beige+brass+oxblood+espresso (without justification)?
- [ ] Italic descender clearance: `leading-[1.1]` min + `pb-1` for y g j p q?
- [ ] Hero fits viewport: headline ≤ 2 lines, subtext ≤ 20 words AND ≤ 4 lines, CTA visible?
- [ ] Hero top padding: max `pt-24` at desktop?
- [ ] Hero stack discipline: max 4 text elements?
- [ ] EYEBROW COUNT: ≤ ceil(sectionCount / 3)?
- [ ] Split-Header Ban: no left headline + right explainer paragraph pattern?
- [ ] Zigzag Alternation Cap: no 3+ consecutive image+text splits?
- [ ] No Duplicate CTA Intent?
- [ ] Logo wall = logos only (no category labels)?
- [ ] Bento Background Diversity: 2-3 cells with real visual variation?
- [ ] "Used by" logo wall UNDER the hero, real SVG logos?
- [ ] Copy Self-Audit: every visible string re-read, no AI-hallucinated phrases?
- [ ] Motion motivated: every animation justified in one sentence?
- [ ] Marquee max-one-per-page?
- [ ] Navigation on ONE line at desktop, height ≤ 80px?
- [ ] Section-Layout-Repetition check: min 4 different layout families across 8 sections?
- [ ] Bento exact cell count (N items = N cells, no empty cells)?
- [ ] Long lists use right UI component (not default `<ul>` for > 5 items)?
- [ ] Real images used (gen-tool → Picsum-seed → explicit placeholder slots)?
- [ ] No pills/labels overlaid on images?
- [ ] No photo-credit captions as decoration?
- [ ] No version footers on marketing pages?
- [ ] No micro-meta-sentences under eyebrows?
- [ ] No decoration text strip at hero bottom?
- [ ] No floating top-right sub-text in section headings?
- [ ] No scoring/progress bars with filled background tracks?
- [ ] No locale/time/weather strips (unless explicitly place-focused)?
- [ ] No scroll cues?
- [ ] No version labels in hero?
- [ ] No section-numbering eyebrows?
- [ ] No decorative dots?
- [ ] No `border-t`+`border-b` on every row?
- [ ] Content density sane: ≤ 25-word sub-paragraphs, no fake-precise specs?
- [ ] Quotes ≤ 3 lines, attribution clean?
- [ ] Motion claimed = motion shown (if `MOTION_INTENSITY > 4`)?
- [ ] GSAP sticky-stack / horizontal-pan per canonical skeleton?
- [ ] No `window.addEventListener('scroll')`?
- [ ] Reduced motion wrapped for `MOTION_INTENSITY > 3`?
- [ ] Dark mode tokens defined and tested?
- [ ] Mobile collapse explicit for high-variance layouts?
- [ ] `min-h-[100dvh]`, never `h-screen`?
- [ ] `useEffect` animations have strict cleanup functions?
- [ ] Empty / loading / error states provided?
- [ ] Icons from allowed library only?
- [ ] Motion isolated in client-leaf components?
- [ ] No AI Tells from Section 9?
- [ ] Core Web Vitals plausibly hit (LCP < 2.5s, INP < 200ms, CLS < 0.1)?
- [ ] One design system per project?

---

## Appendix A - Install Commands
```bash
npm install @material/web
npm install @fluentui/react-components
npm install @carbon/react @carbon/styles
npm install @radix-ui/themes
npx shadcn@latest init
npm install @primer/css
npm install govuk-frontend
npm install uswds
npm install bootstrap
```

## Appendix B - Simple Icons CDN
```
https://cdn.simpleicons.org/{slug}/ffffff   # white
https://cdn.simpleicons.org/{slug}/000000   # black
```

## Appendix C - Apple Liquid Glass Web Approximation
```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}
/* Label in comments: "web glassmorphism approximation, NOT official Apple Liquid Glass" */

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
  }
}
```
