# Chapter 07 Unique ID Generator Lecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Traditional Chinese 30-minute Chapter 07 lecture note that derives Snowflake from distributed ID requirements and briefly compares UUIDv7 and ULID.

**Architecture:** One self-contained Markdown chapter follows the repository's fixed problem-solution-new-problem teaching flow. The first two sections establish requirements and reject unsuitable candidates, the middle sections explain Snowflake's bit layout and generation flow, and the final sections cover failure boundaries and modern alternatives.

**Tech Stack:** Markdown, ASCII diagrams, shell-based structural checks, RFC 9562, the canonical ULID specification, and the repository's existing Chapter 04-06 lecture conventions.

---

## File Structure

- Create: `chapter-07-design-a-unique-id-generator.md` - complete Chapter 07 lecture note.
- Reference: `CLAUDE.md` - required lecture structure and writing conventions.
- Reference: `chapter-04-design-a-rate-limiter.md` - target 30-minute density and Q&A format.
- Reference: `chapter-05-consistent-hashing.md` - causal transitions and discussion-answer format.
- Reference: `docs/superpowers/specs/2026-08-11-chapter-07-unique-id-generator-design.md` - approved scope and acceptance criteria.
- Preserve: `notion-pages.json`, `README.md`, existing chapter files, and quick-guide HTML files.

## Source Boundaries

- Book scope: *System Design Interview - Chapter 07: Design a Unique ID Generator in Distributed Systems*.
- UUID format and UUIDv7: `https://www.rfc-editor.org/rfc/rfc9562.html`.
- ULID format and monotonic behavior: `https://github.com/ulid/spec`.
- Snowflake layout cross-check: the original chapter's `1 + 41 + 5 + 5 + 12` layout; implementation behavior may be checked against `https://github.com/bwmarrin/snowflake`, which documents the original Twitter-style 41-bit timestamp, 10-bit node, and 12-bit sequence layout.

Do not use secondary blog claims for capacity, uniqueness, or ordering guarantees when the book, RFC, or canonical specification covers the same fact.

### Task 1: Establish the document shell and verified fact sheet

**Files:**
- Create: `chapter-07-design-a-unique-id-generator.md`
- Reference: `docs/superpowers/specs/2026-08-11-chapter-07-unique-id-generator-design.md`

- [ ] **Step 1: Confirm the worktree scope before writing**

Run:

```bash
git status --short
```

Expected: no uncommitted changes except this plan file. Do not modify or discard unrelated user changes if any appear.

- [ ] **Step 2: Re-read the approved structure and repository conventions**

Run:

```bash
sed -n '1,240p' CLAUDE.md
sed -n '1,260p' docs/superpowers/specs/2026-08-11-chapter-07-unique-id-generator-design.md
```

Expected: fixed bilingual header, core idea, causal chain, six main sections, problem transitions, two Q&A items per section, four discussion questions, and answer guidance.

- [ ] **Step 3: Record the numerical fact sheet before prose**

Use these checked values consistently throughout the chapter:

```text
1 + 41 + 5 + 5 + 12 = 64 bits
2^41 milliseconds / 1000 / 60 / 60 / 24 / 365 = about 69.7 years
2^5 datacenters = 32
2^5 machines per datacenter = 32
32 * 32 = 1,024 generator nodes
2^12 = 4,096 IDs per node per millisecond
4,096 * 1,000 = 4,096,000 theoretical IDs per node per second
```

State that the per-second number is a format ceiling, not a measured production benchmark.

- [ ] **Step 4: Create the complete Markdown heading shell**

Create the chapter with these headings in this order:

```markdown
# 第七章：設計分散式唯一 ID 生成器
# Chapter 07: Design a Unique ID Generator in Distributed Systems

## 本章的因果鏈
## 1. 為什麼不能只用流水號？
### 面試 Q&A｜唯一 ID 的需求
## 2. 四種候選方案：為什麼最後都不完全符合？
### 面試 Q&A｜候選方案比較
## 3. Snowflake：把資訊放進 64 bits
### 面試 Q&A｜Snowflake 結構
## 4. 一個 Snowflake ID 如何被產生？
### 面試 Q&A｜ID 生成流程
## 5. 容量與故障邊界
### 面試 Q&A｜容量與故障
## 6. 現代補充：UUIDv7、ULID 與 Snowflake 怎麼選？
### 面試 Q&A｜現代方案選型
## 讀書會討論題
## 讀書會討論題參考解答｜面試回答版
```

Add the standard audience, 30-minute estimate, source reference, and a 2-3 sentence core-idea blockquote before the causal chain.

- [ ] **Step 5: Write the causal-chain overview**

Use the approved order exactly:

```text
single database auto increment
  -> multi-master increments
  -> UUID
  -> Ticket Server
  -> Snowflake
  -> clock rollback / sequence exhaustion / machine ID collision
  -> short UUIDv7 and ULID selection note
```

Every arrow must name both the solved problem and the next limitation. Do not present UUIDv7 or ULID before Snowflake.

### Task 2: Write the problem framing and candidate comparison

**Files:**
- Modify: `chapter-07-design-a-unique-id-generator.md`

- [ ] **Step 1: Write Section 1 from a frontend-visible order ID**

Start with an order creation flow and distinguish:

```text
temporary client ID -> supports optimistic UI before the server responds
permanent server ID -> must remain unique across machines and time
```

Define the five requirements: globally unique, 64-bit, roughly increasing with time, low latency/high throughput, and independently generated by multiple nodes. Explicitly state that strict consecutive numbering is not a requirement.

- [ ] **Step 2: Add the Section 1 transition and two Q&A answers**

The transition must ask why database `auto_increment` stops being sufficient when writes are spread across machines.

Q&A topics:

```text
Concept: What requirements does a distributed unique ID need beyond non-duplication?
Decision: When is a database auto-increment key still the right choice?
```

Answers must say that a small single-database system can prefer auto-increment because simplicity may outweigh distributed generation.

- [ ] **Step 3: Write Section 2 as four explicit requirement checks**

For each candidate, show mechanism, benefit, and failed requirement:

| Candidate | Mechanism | Benefit | Limitation under this chapter's requirements |
|---|---|---|---|
| Single DB auto increment | One database increments a counter | Simple, short, ordered | Central bottleneck and failure point |
| Multi-master increment | Different starts and steps | Spreads writes | Reconfiguration and no natural global time order |
| UUIDv4 | Each node generates 128 random-based bits | No central coordination | 128-bit and not time ordered |
| Ticket Server | Central service issues numeric IDs | Short and strictly ordered | Central bottleneck/failure point; HA reintroduces coordination |

Do not claim UUIDv4 has no collision risk; describe collision as extremely unlikely under correct generation rather than impossible.

- [ ] **Step 4: Add the Section 2 transition and two Q&A answers**

The transition must derive the missing combination: local generation like UUID, compact integer representation like database IDs, and rough time ordering without a Ticket Server round trip.

Q&A topics:

```text
Concept: Why does multi-master auto increment not automatically provide global ordering?
Decision: When is UUIDv4 preferable to Snowflake?
```

The UUIDv4 answer should mention independent generation and opaque identifiers, while acknowledging 128-bit storage and random index locality.

### Task 3: Explain Snowflake's bit layout and generation flow

**Files:**
- Modify: `chapter-07-design-a-unique-id-generator.md`

- [ ] **Step 1: Write Section 3 with a concrete 64-bit diagram**

Include this exact field model:

```text
| 0 | 41-bit timestamp | 5-bit datacenter | 5-bit machine | 12-bit sequence |
```

Explain custom epoch before arithmetic. Use a parcel-label analogy: time says when, datacenter and machine say where, sequence says which parcel from that machine in the same millisecond.

- [ ] **Step 2: Walk through every field and its tradeoff**

Cover:

```text
sign bit: keeps the signed 64-bit integer non-negative
timestamp: about 69.7 years from a chosen epoch
datacenter: 32 values
machine: 32 values per datacenter
sequence: 4,096 values per node per millisecond
```

Explain that changing one allocation changes the others; more node bits means fewer timestamp or sequence bits.

- [ ] **Step 3: Add the Section 3 transition and two Q&A answers**

Q&A topics:

```text
Concept: Why does Snowflake include both machine identity and a sequence?
Decision: How would bit allocation change for fewer machines but much higher per-node traffic?
```

The decision answer must say to move bits from node identity to sequence only after calculating required node count and lifetime.

- [ ] **Step 4: Write Section 4 as a stateful generation timeline**

Use an ASCII flow with these branches:

```text
read current millisecond
  -> current > last: reset sequence to 0
  -> current = last: increment sequence
  -> sequence overflow: wait for next millisecond or fail fast
  -> current < last: enter clock rollback handling
combine fields with shifts / bitwise OR
return one 64-bit integer
```

Explain the state each process must retain: last timestamp and current sequence. Do not include production-ready source code.

- [ ] **Step 5: Add the Section 4 transition and two Q&A answers**

Q&A topics:

```text
Concept: Can two Snowflake nodes generate the same ID in the same millisecond?
Decision: Why is machine ID assignment part of the design rather than mere configuration?
```

The concept answer must condition uniqueness on distinct node identity and non-repeated sequence values.

### Task 4: Cover operating boundaries and modern alternatives

**Files:**
- Modify: `chapter-07-design-a-unique-id-generator.md`

- [ ] **Step 1: Write Section 5 capacity calculations**

Show the arithmetic from the Task 1 fact sheet. Present 4,096,000 IDs/second as a theoretical per-node format limit and explicitly distinguish it from an observed benchmark.

- [ ] **Step 2: Write the three required failure scenarios**

Use a problem, consequence, response table:

| Failure | Consequence | Response directions |
|---|---|---|
| Clock rollback | Repeated timestamp can collide or break ordering | Wait for small drift, reject generation, or use guarded logical time |
| Sequence exhaustion | Reusing sequence in one millisecond collides | Wait for next millisecond or return overload; never wrap silently |
| Duplicate machine ID | Two nodes share the same namespace | Allocate IDs centrally or with leases/service discovery and reject duplicates at startup |

Also state that Snowflake IDs are guessable and timestamp-revealing, so they are not authorization tokens or secrets.

- [ ] **Step 3: Add the Section 5 transition and two Q&A answers**

Q&A topics:

```text
Concept: Why can NTP clock correction threaten Snowflake uniqueness?
Decision: Should a generator wait or fail when the clock moves backward?
```

The decision answer must describe the tradeoff: short waits preserve availability for small drift, while large rollback should fail safely or route to a guarded fallback rather than risk duplicates.

- [ ] **Step 4: Write Section 6 as a compact current-options table**

Cross-check UUIDv7 against RFC 9562 and ULID against `ulid/spec`, then compare:

| Option | Size/form | Time sortable | Node ID management | Best fit |
|---|---|---|---|---|
| Snowflake | 64-bit integer | Roughly | Required | Compact high-throughput internal IDs |
| UUIDv7 | 128-bit UUID | Yes by timestamp prefix | Not required | Standard UUID ecosystem and distributed generation |
| ULID | 128-bit, 26-char Base32 | Lexicographically | Not required | Human/log-friendly sortable text IDs |

State that same-millisecond monotonic behavior depends on the UUIDv7/ULID generator implementation and state. Keep this section shorter than the Snowflake layout section.

- [ ] **Step 5: Add the Section 6 Q&A and four discussion questions**

Q&A topics:

```text
Concept: What is the practical difference between UUIDv4 and UUIDv7?
Decision: How do you choose among Snowflake, UUIDv7, and ULID?
```

Discussion scenarios:

```text
1. Optimistic UI temporary ID reconciliation after POST succeeds.
2. Public order IDs must not reveal business volume or timestamps.
3. Offline clients create records before reconnecting.
4. A multi-region service detects a five-second clock rollback.
```

Write an interview-style reference answer for each using requirement, choice, tradeoff, and mitigation. Do not make Snowflake the answer to every scenario.

### Task 5: Verify scope, correctness, and readability

**Files:**
- Verify: `chapter-07-design-a-unique-id-generator.md`
- Preserve: `notion-pages.json`, `README.md`, existing chapters and quick guides.

- [ ] **Step 1: Check file scope and Markdown whitespace**

Run:

```bash
git status --short
git diff --check
git diff --stat
```

Expected: only `chapter-07-design-a-unique-id-generator.md` differs from `HEAD`; no whitespace errors. The plan is committed separately before execution.

- [ ] **Step 2: Verify required sections and Q&A counts**

Run:

```bash
test "$(rg -c '^## [1-6]\.' chapter-07-design-a-unique-id-generator.md)" -eq 6
test "$(rg -c '^### 面試 Q&A' chapter-07-design-a-unique-id-generator.md)" -eq 6
test "$(rg -c '^## 讀書會討論題$' chapter-07-design-a-unique-id-generator.md)" -eq 1
test "$(rg -c '^## 讀書會討論題參考解答' chapter-07-design-a-unique-id-generator.md)" -eq 1
```

Expected: all commands exit 0.

- [ ] **Step 3: Verify code fences and target length**

Run:

```bash
fences=$(rg -c '^```' chapter-07-design-a-unique-id-generator.md)
test $((fences % 2)) -eq 0
chars=$(wc -m < chapter-07-design-a-unique-id-generator.md)
test "$chars" -ge 9000
test "$chars" -le 11000
```

Expected: even fence count and 9,000-11,000 characters.

- [ ] **Step 4: Verify numerical claims independently**

Run:

```bash
node -e "const years=2**41/1000/60/60/24/365; if (years < 69 || years > 70) process.exit(1); if (2**5 * 2**5 !== 1024) process.exit(1); if (2**12 * 1000 !== 4096000) process.exit(1); console.log({years,nodes:1024,idsPerMs:4096,idsPerSecond:4096000})"
```

Expected: exit 0 and output showing about 69.7 years, 1,024 nodes, 4,096 IDs/ms, and 4,096,000 IDs/s.

- [ ] **Step 5: Scan for placeholders and semantic overclaims**

Run:

```bash
rg -n 'TB[D]|TO[D]O|FIXM[E]|絕對不會碰撞|嚴格遞增|保證無法猜測|實際每秒.*4,096,000' chapter-07-design-a-unique-id-generator.md
```

Expected: no matches. Then read the chapter from top to bottom and confirm every technical name is introduced after its problem, every section has a transition, and the modern comparison remains shorter than the Snowflake explanation.

- [ ] **Step 6: Commit the verified lecture note**

Run:

```bash
git add chapter-07-design-a-unique-id-generator.md
git commit -m "docs: add chapter 7 unique ID generator notes"
```

Expected: one commit containing only the new lecture note. Verify with `git show --stat --oneline HEAD` and `git status --short`.
