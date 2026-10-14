# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A series of system design lecture notes in Traditional Chinese, aimed at frontend engineers. Each chapter is a self-contained 30-minute session. The reference book is *System Design Interview – An Insider's Guide, Vol.1*.

## Chapter File Naming

Files follow the pattern `chapter-NN-kebab-case-title.md`. Chapters written so far:
- `chapter-01-scale-from-zero-to-millions.md` ✅
- `chapter-02-back-of-the-envelope-estimation.md` ✅
- `chapter-03-system-design-interview-framework.md` ✅
- `chapter-04-design-a-rate-limiter.md` ✅
- `chapter-05` through `chapter-10` ✅ (see the files in the repo root)

Chapters 11–15 are documented in README.md but not yet written.

## Lecture Note Format

Every chapter must follow this exact structure:

1. **Header block** — bilingual title (Chinese + English), audience, time estimate, source reference
2. **核心思路 (Core idea)** — a blockquote stating the chapter's central insight in 2–3 sentences
3. **本章的因果鏈 (Causal chain)** — an ASCII diagram showing the problem→solution→new-problem progression that drives the whole chapter
4. **Sections with ⚠️ transitions** — each major section opens by referencing the problem left by the previous section, then introduces the solution
5. **面試 Q&A** — 2 questions per section: one conceptual ("什麼是 X？") and one decision-based ("什麼時候用 X？")
6. **讀書會討論題 (Discussion questions)** — 4 scenario questions grounded in frontend engineers' daily experience

## Pipeline-Type Chapters (CH09, 10, 14, 15)

Chapters that describe a pipeline of components that all exist at once (crawler, notification, YouTube, Google Drive) use a different format. Evolution-type chapters (CH01–08, 11–13) keep the format above.

- **Two files:** a simplified `chapter-NN-design-a-xxx.md` (pushed to Notion, links to the HTML) and an interactive `chapter-NN-xxx-interactive.html` (same shared design system and verification steps as the quick guides, plus the demos below).
- **Order:** 核心思路 → trace one request through the pipeline → component breakdown (analogy + trade-off) → 真實系統怎麼取捨 → 面試模擬 (3–4 questions) → 討論題 → 因果鏈 last, as a visual recap.
- **Demos are inline SVG + vanilla JS step-through**, no libraries: a "next step" button moves a dot through the components. Respect `prefers-reduced-motion`, keep wide SVGs in a horizontally scrollable wrapper on mobile, and never put user input into `innerHTML`.
- **Real-system claims** (Scrapy, Googlebot, etc.) must be checked against official docs before publishing.

## Content Conventions

- **Language:** Traditional Chinese body text; technical terms appear as Chinese + English in parentheses on first use (e.g., 快取（Cache）)
- **Diagrams:** Use ASCII art with `→`, `↓`, `[方括號]` for components; keep them inside fenced code blocks
- **Analogies:** Each major concept gets a life/frontend analogy before the technical explanation (marked with 🏗️ or similar emoji)
- **Tone:** Conversational, not textbook — write as if explaining to a colleague, not writing documentation
- **Causal framing:** Never introduce a technology without first stating the problem it solves; the ⚠️ emoji marks these transitions

## The Three-Stage Curriculum Arc

Later chapters reference components introduced in earlier ones — re-explain by name only, don't re-introduce from scratch.

**Stage 1 — Foundation (CH01–03):** How systems evolve, how to size them with numbers, how to structure a design interview.

**Stage 2 — Building Blocks (CH04–08):** Reusable components for distributed systems:
- CH04 Rate Limiter → CH05 Consistent Hashing → CH06 Key-Value Store → CH07 Unique ID Generator → CH08 URL Shortener

**Stage 3 — Real Systems (CH09–15):** Composing the above into full product systems:
- CH09–10 async background processing (crawlers, notifications)
- CH11–12 social interaction at scale (news feed, chat)
- CH13 latency-sensitive search (autocomplete)
- CH14–15 binary media storage (YouTube, Google Drive)

## Notion Sync

`notion-pages.json` tracks the Notion page ID for each chapter file and the target database ID. It is written automatically by the `notion-push` skill — do not edit it by hand.

## Quick-Guide HTML Artifacts

Alongside a written chapter, a standalone HTML "quick guide" can be built as a faster (8–10 minute) companion read. Existing examples: `chapter-05-consistent-hashing-quick-guide.html`, `chapter-06-key-value-store-quick-guide.html`, `chapter-07-unique-id-generator-quick-guide.html`.

**File:** `chapter-NN-topic-quick-guide.html`, single self-contained file (inline CSS + vanilla JS, no build step, no external dependencies, no network calls). The original chapter `.md` file is never modified.

**Reuse the shared design system verbatim** for series consistency — same CSS custom properties, layout, and script every time:

```css
:root {
  --paper: #f7f8f5; --surface: #ffffff; --ink: #17201b; --muted: #5e6a63;
  --line: #d8ddd9; --problem: #b4473a; --solution: #16745b;
  --system: #245f9e; --warning: #9a6a12;
}
```

- `.shell` CSS Grid: sticky sidebar nav on desktop, horizontal-scroll nav on mobile (`@media (max-width: 780px)`).
- Each concept section follows: `.eyebrow` (現在的問題) → `<h2>` → `.concept-grid` with `aria-label="怎麼做"` / `aria-label="代價"` panels → `.takeaway` one-liner.
- Diagrams as `<pre class="diagram">` ASCII blocks; comparison tables as plain `<table>`.
- Ends with a problem/solution/cost summary `<table>` and 3 `<details>`/`<summary>` self-check questions (collapsed by default).
- Nav active-state via `IntersectionObserver` (guarded by `'IntersectionObserver' in window`), `:focus-visible` outlines, `prefers-reduced-motion`-guarded reveal animation, `js` class added only via script for progressive enhancement.

**Verification before publishing:**
1. `shasum` the original chapter file before and after — must be unchanged; `git diff` on it and on `notion-pages.json` must be empty.
2. `rg` check that all section IDs, the `<details>` blocks, and `IntersectionObserver` are present; confirm no `https?://` or external `src`/`href` references.
3. Extract the inline `<script>` and run `node --check` on it.
4. Serve locally (`python3 -m http.server`, since Playwright MCP blocks `file://`) and check desktop (1440×900) and mobile (390×844) screenshots, plus a click-to-expand test on one `<details>`.
5. Commit only the new HTML file (and a design spec if one was written) — never `notion-pages.json`.
6. Publish via the `Artifact` tool for a shareable link.
