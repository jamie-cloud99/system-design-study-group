# Chapter 07 ELI15 HTML Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a standalone 15-minute Traditional Chinese HTML guide that follows one order through a distributed system, derives Snowflake from real collision problems, and ends with practical ID selection exercises.

**Architecture:** One self-contained HTML file owns content, styling, and progressive interactions. Six story sections form a single vertical journey; native HTML fallbacks keep all explanations readable without JavaScript, while small vanilla JavaScript controllers enhance Snowflake field exploration, scenario feedback, and active navigation.

**Tech Stack:** Semantic HTML5, inline CSS, vanilla JavaScript, native `details/summary`, `IntersectionObserver`, shell-based content checks, and Playwright browser verification.

---

## File Structure

- Create: `chapter-07-unique-id-generator-eli15.html` - complete story, responsive styles, diagrams, native fallbacks, and progressive interactions.
- Reference: `docs/superpowers/specs/2026-08-26-chapter-07-eli15-html-design.md` - approved narrative, visuals, interaction, and acceptance criteria.
- Reference: `chapter-07-unique-id-generator-quick-guide.html` - series color tokens, responsive shell, focus treatment, and progressive navigation pattern.
- Preserve: `chapter-07-design-a-unique-id-generator.md` - existing 30-minute source.
- Preserve: `chapter-07-unique-id-generator-quick-guide.html` - existing 10-minute guide.
- Preserve: `notion-pages.json` - committed mapping inside the feature worktree. The main worktree's pre-existing uncommitted Chapter 07 entry remains isolated and must still be present after integration.

## Baseline Protection

The implementation must preserve these current SHA-1 values:

```text
93e8eb365b574f9a4ce8e43685da376fb0322cd8  chapter-07-design-a-unique-id-generator.md
8b829ec85cc64497d00a3d23e0bc4b3beaaa6842  chapter-07-unique-id-generator-quick-guide.html
e59a566eeca1dd9f8802bbf9d831497255c5c3f8  notion-pages.json
```

### Task 1: Establish the standalone document and story

**Files:**
- Create: `chapter-07-unique-id-generator-eli15.html`
- Reference: `docs/superpowers/specs/2026-08-26-chapter-07-eli15-html-design.md`

- [x] **Step 1: Run the acceptance checks before the file exists**

Run:

```bash
test -f chapter-07-unique-id-generator-eli15.html
rg -q 'id="order-start"' chapter-07-unique-id-generator-eli15.html
rg -q 'id="choose"' chapter-07-unique-id-generator-eli15.html
```

Expected: FAIL because the new HTML does not exist yet.

- [x] **Step 2: Reconfirm protected-file hashes**

Run:

```bash
shasum chapter-07-design-a-unique-id-generator.md chapter-07-unique-id-generator-quick-guide.html notion-pages.json
```

Expected: output exactly matches the three hashes in **Baseline Protection**.

- [x] **Step 3: Create the semantic document shell**

Create one `<!doctype html>` document with:

```html
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>唯一 ID 到底用在哪裡？｜Chapter 07 ELI15</title>
</head>
<body>
  <div class="shell">
    <nav class="journey-nav" aria-label="訂單 ID 的旅程">
      <a href="#order-start">按下購買</a>
      <a href="#collision">三台撞號</a>
      <a href="#attempts">四次嘗試</a>
      <a href="#snowflake">拆開 Snowflake</a>
      <a href="#failures">現實故障</a>
      <a href="#choose">情境選型</a>
    </nav>
    <main>
      <section id="order-start" class="story-section"></section>
      <section id="collision" class="story-section"></section>
      <section id="attempts" class="story-section"></section>
      <section id="snowflake" class="story-section"></section>
      <section id="failures" class="story-section"></section>
      <section id="choose" class="story-section"></section>
    </main>
  </div>
</body>
</html>
```

Each section starts with a `SCENE NN` eyebrow and one literal question as its `h2`. Do not add a marketing hero or feature-description copy.

- [x] **Step 4: Write Scene 1 and Scene 2 as one continuous order flow**

Scene 1 must show:

```text
小明按下購買
  -> 前端先建立 temp_order_8f3
  -> POST /orders
  -> 後端建立永久訂單
  -> 前端用 permanent ID 替換 temporary ID
```

Explain the practical responsibilities:

```text
temporary ID: keeps one optimistic UI row stable before the response
permanent ID: links order, payment, shipment, support ticket, and audit log for years
```

Scene 2 must show a CSS/HTML system diagram:

```text
10,000 buyers -> Load Balancer -> Order Server A / B / C -> Orders DB
```

Use a native `details` prompt asking what happens if A, B, and C each issue `101`. The revealed answer must name real consequences: duplicate primary key errors, a payment attached to the wrong order, or a support lookup returning the wrong record.

- [x] **Step 5: Write Scene 3 as four attempts, each tied to the same order**

Use four unframed full-width attempt rows:

| Attempt | What it fixes | What still hurts |
|---|---|---|
| Database auto increment | One counter prevents duplicates | Every write depends on one database, but this is still best for a small single-database app |
| Odd/even multi-master | Two databases can issue different ranges | Adding a third database changes the numbering rule; ID size does not represent global creation order |
| UUIDv4 | Every server can create IDs locally | 128-bit random form misses this chapter's compact 64-bit and rough time-order requirements |
| Ticket Server | Produces short ordered numbers | Every order again waits for a central service; high availability reintroduces coordination |

End with this missing combination:

```text
local generation + compact integer + rough time order + no per-order central round trip
```

- [x] **Step 6: Run the story acceptance checks**

Run:

```bash
test "$(rg -c 'class="story-section"' chapter-07-unique-id-generator-eli15.html)" -eq 6
rg -q 'temp_order_8f3' chapter-07-unique-id-generator-eli15.html
rg -q 'Order Server A' chapter-07-unique-id-generator-eli15.html
rg -q 'Database auto increment' chapter-07-unique-id-generator-eli15.html
rg -q 'UUIDv4' chapter-07-unique-id-generator-eli15.html
rg -q 'Ticket Server' chapter-07-unique-id-generator-eli15.html
```

Expected: all commands exit 0.

### Task 2: Derive Snowflake and connect it to failures

**Files:**
- Modify: `chapter-07-unique-id-generator-eli15.html`

- [x] **Step 1: Write Scene 4 from meaning to bits**

Introduce Snowflake as a parcel label:

```text
timestamp: when this order was created
node identity: which generator created it
sequence: which order this node handled in the same millisecond
```

Only after those meanings are clear, show a stable-width bit band:

```text
| 0 | 41-bit timestamp | 5-bit datacenter | 5-bit machine | 12-bit sequence |
1 + 41 + 5 + 5 + 12 = 64 bits
```

Explain that `datacenter + machine` together are one node identity. Explain that Snowflake reduces coordination from every order to node assignment at deployment time; it does not eliminate coordination entirely.

- [x] **Step 2: Add the progressive Snowflake field explorer**

Add three buttons:

```html
<div class="part-controls" role="group" aria-label="Snowflake 欄位">
  <button type="button" data-part="timestamp" aria-pressed="true">時間</button>
  <button type="button" data-part="node" aria-pressed="false">機器身分</button>
  <button type="button" data-part="sequence" aria-pressed="false">同毫秒序號</button>
</div>
<div id="part-explanation" class="part-explanation" aria-live="polite"></div>
```

Use this exact data contract in the script:

```javascript
var partCopy = {
  timestamp: {
    title: '時間：讓新資料大致排在後面',
    body: '同一台機器進入新的毫秒時，sequence 會重新從 0 開始。',
    example: '20:00:00.120'
  },
  node: {
    title: '機器身分：讓不同伺服器使用不同號碼空間',
    body: 'datacenter 與 machine 的組合不能同時分配給兩台生成器。',
    example: '台北機房 / 第 7 台'
  },
  sequence: {
    title: '序號：分開同一台機器、同一毫秒的多筆訂單',
    body: '12 bits 提供 0 到 4095；用完就等下一毫秒或分流。',
    example: '第 0、1、2 筆'
  }
};
```

Clicking a button must update `aria-pressed`, the bit-band selected style, and the fixed-size explanation region without changing its height.

- [x] **Step 3: Write Scene 5 as three concrete failure stories**

Use a problem/consequence/response table or three full-width rows:

```text
Clock rollback:
  20:00:00.500 -> clock changes to 20:00:00.480
  risk: reuse of an earlier timestamp/sequence range
  response: wait for tiny drift; reject and route elsewhere for large rollback

Sequence exhaustion:
  request 4097 arrives in the same millisecond
  risk: wrapping to 0 duplicates an earlier combination
  response: wait for the next millisecond or return overload

Duplicate node identity:
  Server A and B both use datacenter=3, machine=7
  risk: both generate in the same namespace
  response: lease/assign identity and reject startup conflicts
```

Add a frontend warning:

```text
API: { "id": "1541815603606036480" }
Keep it as a string. JavaScript Number is only safe through 2^53 - 1.
```

- [x] **Step 4: Verify numerical and semantic claims**

Run:

```bash
rg -q '1 + 41 + 5 + 5 + 12 = 64' chapter-07-unique-id-generator-eli15.html
rg -q '4,096' chapter-07-unique-id-generator-eli15.html
rg -q '2\^53 - 1' chapter-07-unique-id-generator-eli15.html
rg -q '不是完全不協調' chapter-07-unique-id-generator-eli15.html
node -e "if (2**5 * 2**5 !== 1024 || 2**12 !== 4096) process.exit(1)"
```

Expected: all commands exit 0.

### Task 3: Add practical selection exercises and responsive presentation

**Files:**
- Modify: `chapter-07-unique-id-generator-eli15.html`

- [x] **Step 1: Write the four Scene 6 choices**

Use four `.choice-question` groups. Each group provides 2-3 buttons with `data-feedback`; one recommended answer must explain both fit and tradeoff:

| Scenario | Recommendation | Required explanation |
|---|---|---|
| Small internal admin app with one database | Database auto increment | Simplest option; no distributed generator operation |
| Offline note app creates records without a server | UUIDv7 or ULID | Local generation without machine ID; business conflicts still need handling |
| High-volume internal order/event writes require compact 64-bit IDs | Snowflake | Local high-throughput generation and rough time order; operates clocks and node identity |
| Public order URL must not reveal time or volume | Separate opaque public ID | Snowflake may remain internal; authorization is still mandatory |

Each group also contains a `details.choice-fallback` with the complete recommendation for no-JavaScript readers.

- [x] **Step 2: Implement choice feedback**

Use delegated click handling:

```javascript
document.querySelectorAll('.choice-question').forEach(function (question) {
  var output = question.querySelector('.choice-feedback');
  question.querySelectorAll('button[data-feedback]').forEach(function (button) {
    button.addEventListener('click', function () {
      question.querySelectorAll('button[data-feedback]').forEach(function (candidate) {
        candidate.setAttribute('aria-pressed', String(candidate === button));
      });
      output.textContent = button.getAttribute('data-feedback');
    });
  });
});
```

Only hide `.choice-fallback` after the script adds `.js` to the root element.

- [x] **Step 3: Add the story-scroll design system**

Define the existing series tokens exactly:

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

Desktop requirements:

```css
.shell {
  display: grid;
  grid-template-columns: 13rem minmax(0, 48rem);
  gap: 3rem;
  max-width: 68rem;
  margin: 0 auto;
}
.journey-nav {
  position: sticky;
  top: 1.5rem;
  align-self: start;
}
```

Mobile at `max-width: 780px`:

```css
.shell { display: block; }
.journey-nav {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  overflow-x: auto;
}
```

Also implement:

- `letter-spacing: 0` globally.
- 8px or smaller corner radii.
- `:focus-visible` outlines.
- stable minimum heights for `.part-explanation` and `.choice-feedback`.
- overflow containment for the bit band, tables, and system diagrams.
- no gradients, external media, decorative blobs, or nested cards.
- `prefers-reduced-motion` gating for small reveal transitions.

- [x] **Step 4: Add progressive active navigation**

```javascript
var navLinks = Array.prototype.slice.call(document.querySelectorAll('.journey-nav a'));
if ('IntersectionObserver' in window) {
  var observer = new IntersectionObserver(function (entries) {
    var visible = entries
      .filter(function (entry) { return entry.isIntersecting; })
      .sort(function (a, b) { return b.intersectionRatio - a.intersectionRatio; })[0];
    if (!visible) return;
    navLinks.forEach(function (link) { link.removeAttribute('aria-current'); });
    var active = navLinks.find(function (link) {
      return link.hash === '#' + visible.target.id;
    });
    if (active) active.setAttribute('aria-current', 'location');
  }, { rootMargin: '-20% 0px -65%', threshold: [0, 0.2, 0.6] });
  document.querySelectorAll('main > section[id]').forEach(function (section) {
    observer.observe(section);
  });
}
```

- [x] **Step 5: Run static structure and script checks**

Run:

```bash
test "$(rg -c 'class="choice-question"' chapter-07-unique-id-generator-eli15.html)" -eq 4
test "$(rg -c 'class="story-section"' chapter-07-unique-id-generator-eli15.html)" -eq 6
rg -q 'data-part="timestamp"' chapter-07-unique-id-generator-eli15.html
rg -q 'aria-live="polite"' chapter-07-unique-id-generator-eli15.html
rg -q 'IntersectionObserver' chapter-07-unique-id-generator-eli15.html
rg -q 'prefers-reduced-motion' chapter-07-unique-id-generator-eli15.html
test -z "$(rg -n 'https?://|src="[^"]+"|href="https?://' chapter-07-unique-id-generator-eli15.html)"
```

Extract the inline script to a temporary file and check syntax:

```bash
perl -0777 -ne 'print $1 if /<script>(.*?)<\/script>/s' chapter-07-unique-id-generator-eli15.html > /tmp/ch7-eli15-script.js
node --check /tmp/ch7-eli15-script.js
```

Expected: all commands exit 0 and Node reports no syntax error.

### Task 4: Verify behavior, layout, and protected scope

**Files:**
- Verify: `chapter-07-unique-id-generator-eli15.html`
- Preserve: `chapter-07-design-a-unique-id-generator.md`
- Preserve: `chapter-07-unique-id-generator-quick-guide.html`
- Preserve: `notion-pages.json`

- [x] **Step 1: Start an isolated local preview**

Inspect port ownership, then serve the repository:

```bash
lsof -nP -iTCP:8283 -sTCP:LISTEN
python3 -m http.server 8283 --bind 127.0.0.1
```

Expected: use port 8283 only if the ownership check shows it is free; otherwise choose another free port and record it.

- [x] **Step 2: Run desktop Playwright verification**

Open:

```text
http://127.0.0.1:8283/chapter-07-unique-id-generator-eli15.html
```

At 1440x900:

- confirm six nav items and six sections render;
- click the node-identity Snowflake button and verify the explanation mentions `datacenter` and `machine`;
- answer each of four selection questions and verify its feedback region changes;
- expand a `details` prompt;
- assert `document.documentElement.scrollWidth === document.documentElement.clientWidth`;
- assert no console errors;
- save screenshot to `/tmp/ch7-eli15-desktop.png`.

- [x] **Step 3: Run mobile Playwright verification**

At 390x844:

- verify the journey nav is horizontal and the main document scrolls vertically;
- verify no heading, button, bit label, or feedback text overlaps;
- click the sequence field and verify feedback remains visible;
- expand a prompt and answer one selection question;
- assert no page-level horizontal overflow;
- save screenshot to `/tmp/ch7-eli15-mobile.png`.

- [x] **Step 4: Inspect screenshots and canvas/page pixels**

Open both screenshots and confirm:

```text
desktop: sticky journey rail visible, content uses the available width, no nested-card appearance
mobile: next section is naturally reachable, nav does not cover the scene heading, long labels wrap
both: diagrams and bit band are nonblank, selected states are distinguishable without layout shift
```

If browser checks reveal a defect, correct the smallest relevant HTML/CSS/JavaScript region and rerun both viewport checks.

- [x] **Step 5: Run final protected-scope verification**

Run:

```bash
shasum chapter-07-design-a-unique-id-generator.md chapter-07-unique-id-generator-quick-guide.html notion-pages.json
git diff --check
git status --short
git diff -- chapter-07-design-a-unique-id-generator.md chapter-07-unique-id-generator-quick-guide.html notion-pages.json
```

Expected hashes:

```text
93e8eb365b574f9a4ce8e43685da376fb0322cd8  chapter-07-design-a-unique-id-generator.md
8b829ec85cc64497d00a3d23e0bc4b3beaaa6842  chapter-07-unique-id-generator-quick-guide.html
e59a566eeca1dd9f8802bbf9d831497255c5c3f8  notion-pages.json
```

Expected feature-worktree state: only the corrected plan and new HTML differ; `notion-pages.json` and both original Chapter 07 content files are clean. After integrating the feature branch, separately verify that the main worktree still has its pre-existing Chapter 07 mapping diff and SHA-1 `2754f7b3dd7df78f19c23e7aaa0879da12124b7e`.

- [x] **Step 6: Review the final content against the three learning outcomes**

Read the guide from top to bottom and verify it explicitly answers:

```text
Why do multiple servers make a simple counter difficult?
What collision does each Snowflake field prevent?
Which real scenarios should not use Snowflake?
```

Expected: each answer appears in the story before the final selection exercise; no section requires memorizing terminology before seeing its application.
