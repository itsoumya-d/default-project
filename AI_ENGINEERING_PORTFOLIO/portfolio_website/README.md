# Portfolio Website — Executive Hub, Not a Gallery

**Status:** scaffold. No page is built or deployed.

The site is the 60-second triage surface for a recruiter or hiring manager. It
links to reproducible artifacts; it does not replace them. The platform decision
is in `../PLATFORM_STRATEGY.md`.

## Required pages

| Page | Content | Evidence rule |
|---|---|---|
| Home | one-sentence positioning, six pinned projects, current focus | no skill percentage bars |
| Case study ×5 | problem → constraint → design → failure → measured result | every number links to a log or artifact |
| Project index | all ten projects, status labels (`shipped`, `in progress`, `spec`) | no "coming soon" without a date |
| About | background, constraints, contact | no invented credentials |
| Notes | post-mortems, one per shipped project | canonical Markdown, cross-posted |

## Build plan

1. Static export (Astro or Next.js `output: "export"`) so it runs on GitHub Pages
   or Cloudflare Pages without a server.
2. Content in Markdown, one file per case study, typed front matter.
3. Lighthouse ≥98 on mobile; no client-side data fetching for the home page.
4. Embed the HF Spaces and the W&B report only after they are public.
5. Add a build check that fails on a missing evidence link.

## Non-goals

- A generic chatbot widget.
- Testimonials or logos that are not real.
- A blog cadence that competes with project work.
