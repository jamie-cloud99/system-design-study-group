# Chapter 06 Learning Artifact Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone, responsive HTML artifact that teaches the essential Chapter 06 Key-Value Store concepts in about ten minutes（約 10 分鐘）.

**Architecture:** A single semantic HTML document contains the learning content, inline CSS, and a small inline script. Sections follow one repeated teaching pattern and are connected by a sticky progress navigation; native details elements provide accessible self-check answers without adding a framework or build step.

**Tech Stack:** HTML5, CSS, vanilla JavaScript, Node.js verification, Playwright browser screenshots when available.

---

## File Structure

- Create: `chapter-06-key-value-store-quick-guide.html` - complete standalone artifact.
- Preserve: `chapter-06-design-a-key-value-store.md` - original source must remain unchanged.
- Preserve: `notion-pages.json` - artifact work must not change Notion mappings.

### Task 1: Create the semantic learning flow

**Files:**
- Create: `chapter-06-key-value-store-quick-guide.html`

- [ ] **Step 1: Record the original chapter checksum**

Run:

```bash
shasum chapter-06-design-a-key-value-store.md
```

Expected: one SHA-1 value to compare during final verification.

- [ ] **Step 2: Create the standalone document structure**

Use one `main` element with these section IDs and navigation targets:

```html
<nav aria-label="章節導覽">
  <a href="#recap">Recap</a>
  <a href="#partition">分片</a>
  <a href="#replication">複製</a>
  <a href="#consistency">一致性</a>
  <a href="#conflict">衝突</a>
  <a href="#recovery">修復</a>
  <a href="#storage">儲存</a>
</nav>
<main>
  <section id="recap"></section>
  <section id="partition"></section>
  <section id="replication"></section>
  <section id="consistency"></section>
  <section id="conflict"></section>
  <section id="recovery"></section>
  <section id="storage"></section>
  <section id="summary"></section>
  <section id="check"></section>
</main>
```

- [ ] **Step 3: Write the recap before technical terms**

Include the familiar model and three constraints before mentioning CAP or Quorum:

```text
put(key, value) / get(key)
Client -> Memory -> Disk
資料會多到一台放不下 / 機器一定會壞 / 網路可能中斷
```

- [ ] **Step 4: Write all six concept sections in a repeated format**

Each section must visibly include:

```html
<p class="eyebrow">現在的問題</p>
<h2>白話問題標題</h2>
<div class="concept-grid">
  <section aria-label="怎麼做">...</section>
  <section aria-label="代價">...</section>
</div>
<p class="takeaway"><strong>一句話：</strong>...</p>
```

Explain plain language first, with technical names in secondary labels. Keep Vector Clock, Gossip, Hinted Handoff, Merkle Tree, LSM-Tree, and Bloom Filter at purpose-only depth.

- [ ] **Step 5: Add summary and three self-check questions**

Use a compact problem/solution/tradeoff table followed by native disclosure controls:

```html
<details>
  <summary>為什麼資料有副本之後，系統反而多了一個問題？</summary>
  <p>因為多台機器上的同一筆資料可能不是同一個版本。</p>
</details>
```

### Task 2: Build the visual system and diagrams

**Files:**
- Modify: `chapter-06-key-value-store-quick-guide.html`

- [ ] **Step 1: Define a restrained multi-color token system**

Use CSS custom properties with neutral paper, ink, red problem, green solution, blue system, and yellow warning colors:

```css
:root {
  --paper: #f7f8f5;
  --surface: #ffffff;
  --ink: #17201b;
  --muted: #5e6a63;
  --line: #d8ddd9;
  --problem: #b4473a;
  --solution: #16745b;
  --system: #245f9e;
  --warning: #9a6a12;
}
```

Do not use gradients, decorative orbs, excessive shadows, negative letter spacing, or viewport-scaled type.

- [ ] **Step 2: Create stable responsive layout rules**

Desktop uses a narrow sticky sidebar plus a readable content column; mobile（手機版）uses a sticky horizontal nav and a single column:

```css
.shell { display: grid; grid-template-columns: 13rem minmax(0, 48rem); gap: 3rem; }
@media (max-width: 780px) {
  .shell { display: block; }
  .progress-nav { display: flex; overflow-x: auto; }
}
```

- [ ] **Step 3: Build CSS diagrams as actual learning visuals**

Create three stable diagrams using semantic HTML and CSS:

- Single machine: Client -> Memory -> Disk
- Replication: one write reaching three replicas, with one delayed node
- Storage path: Commit Log -> MemTable -> SSTable, with Bloom Filter before disk lookup

Every diagram must have an accessible text label and must not rely on color alone.

- [ ] **Step 4: Add restrained motion and focus styles**

Use a short section reveal only when motion is allowed:

```css
@media (prefers-reduced-motion: no-preference) {
  .concept-section { animation: reveal 320ms ease-out both; }
}
:focus-visible { outline: 3px solid #245f9e; outline-offset: 3px; }
```

### Task 3: Add navigation state and accessible interaction

**Files:**
- Modify: `chapter-06-key-value-store-quick-guide.html`

- [ ] **Step 1: Add scroll-aware navigation state**

Use `IntersectionObserver` to apply `aria-current="location"` to the active section link. The script must fail harmlessly when the API is unavailable.

```js
const links = [...document.querySelectorAll('.progress-nav a')];
const byId = new Map(links.map(link => [link.hash.slice(1), link]));
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;
    links.forEach(link => link.removeAttribute('aria-current'));
    byId.get(visible.target.id)?.setAttribute('aria-current', 'location');
  }, { rootMargin: '-20% 0px -65%', threshold: [0, 0.2, 0.6] });
  document.querySelectorAll('main > section[id]').forEach(section => observer.observe(section));
}
```

- [ ] **Step 2: Keep self-check interaction native**

Use `details` and `summary` rather than custom button state so keyboard（鍵盤）, screen reader, and no-JavaScript behavior remain functional.

- [ ] **Step 3: Add progressive enhancement markers**

Add a `js` class to the root only from JavaScript, and ensure all content remains visible without it.

### Task 4: Verify structure, behavior, and responsive rendering

**Files:**
- Verify: `chapter-06-key-value-store-quick-guide.html`
- Preserve: `chapter-06-design-a-key-value-store.md`

- [ ] **Step 1: Run static content checks**

Run:

```bash
rg -n 'id="(recap|partition|replication|consistency|conflict|recovery|storage|summary|check)"|<details>|IntersectionObserver' chapter-06-key-value-store-quick-guide.html
```

Expected: all nine section IDs, three `details` blocks, and the observer implementation.

- [ ] **Step 2: Check inline JavaScript syntax**

Extract the inline script to a temporary file and run:

```bash
sed -n '/<script>/,/<\/script>/p' chapter-06-key-value-store-quick-guide.html | sed '1d;$d' > /tmp/ch6-artifact-script.js
node --check /tmp/ch6-artifact-script.js
```

Expected: exit code 0 with no syntax errors.

- [ ] **Step 3: Verify isolation and offline behavior**

Run:

```bash
rg -n 'https?://|src="[^#]|href="https?://' chapter-06-key-value-store-quick-guide.html
git diff -- chapter-06-design-a-key-value-store.md notion-pages.json
shasum chapter-06-design-a-key-value-store.md
```

Expected: no external dependency matches; artifact work adds no diff to the original chapter or Notion mapping; checksum matches Task 1.

- [ ] **Step 4: Inspect desktop and mobile screenshots**

Open the local HTML with Playwright at 1440x900 and 390x844. Confirm the first viewport contains recap content, diagrams are nonblank, text does not overlap, the navigation remains usable, and all three self-check answers expand.

- [ ] **Step 5: Commit the artifact only**

```bash
git add chapter-06-key-value-store-quick-guide.html
git commit -m "feat: add chapter 6 learning artifact"
```
