# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A series of system design lecture notes in Traditional Chinese, aimed at frontend engineers. Each chapter is a self-contained 30-minute session. The reference book is *System Design Interview – An Insider's Guide, Vol.1*.

## Chapter File Naming

Files follow the pattern `chapter-NN-kebab-case-title.md`. Existing chapters:
- `chapter-01-scale-from-zero-to-millions.md` ✅
- `chapter-02-back-of-the-envelope-estimation.md` ✅ (in progress)

Chapters 03–15 are documented in README.md but not yet written.

## Lecture Note Format

Every chapter must follow this exact structure:

1. **Header block** — bilingual title (Chinese + English), audience, time estimate, source reference
2. **核心思路 (Core idea)** — a blockquote stating the chapter's central insight in 2–3 sentences
3. **本章的因果鏈 (Causal chain)** — an ASCII diagram showing the problem→solution→new-problem progression that drives the whole chapter
4. **Sections with ⚠️ transitions** — each major section opens by referencing the problem left by the previous section, then introduces the solution
5. **面試 Q&A** — 2 questions per section: one conceptual ("什麼是 X？") and one decision-based ("什麼時候用 X？")
6. **讀書會討論題 (Discussion questions)** — 4 scenario questions grounded in frontend engineers' daily experience

## Content Conventions

- **Language:** Traditional Chinese body text; technical terms appear as Chinese + English in parentheses on first use (e.g., 快取（Cache）)
- **Diagrams:** Use ASCII art with `→`, `↓`, `[方括號]` for components; keep them inside fenced code blocks
- **Analogies:** Each major concept gets a life/frontend analogy before the technical explanation (marked with 🏗️ or similar emoji)
- **Tone:** Conversational, not textbook — write as if explaining to a colleague, not writing documentation
- **Causal framing:** Never introduce a technology without first stating the problem it solves; the ⚠️ emoji marks these transitions

## The Three-Stage Curriculum Arc

Chapters are grouped into three stages (see README.md), and later chapters reference earlier ones. When writing a new chapter, check what components were introduced in prior chapters and reference them by name rather than re-explaining them.
