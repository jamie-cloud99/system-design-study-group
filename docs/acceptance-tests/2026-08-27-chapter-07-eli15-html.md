# Acceptance Tests: Chapter 07 ELI15 HTML Guide
> Generated: 2026-08-27 | Status: verified 2026-08-27

Test 1 [E2E] (Happy path): At 1440x900, open the standalone guide, follow all six journey links, expand one "先猜猜看", select each Snowflake field, and answer all four scenario questions -> every section is reachable, field explanations update in place, and every scenario returns a recommendation with a tradeoff.

Test 2 [E2E] (Error - JavaScript unavailable): Disable JavaScript and reload the page -> the six-section story remains readable, each "先猜猜看" can be expanded, and all four scenario recommendations remain available through native details without an empty or broken interaction area.

Test 3 [E2E] (Error - IntersectionObserver unavailable): Remove or stub `window.IntersectionObserver` before page script execution -> journey links still navigate to their matching section anchors and no console error prevents Snowflake or scenario controls from working.

Test 4 [E2E] (Error - network unavailable): Open the downloaded HTML while offline -> typography, colors, diagrams, story content, and interactions render without external requests or missing assets.

Test 5 [E2E] (Edge - 390x844 mobile): At 390x844, scroll through the full page, use the horizontal journey navigation, select the sequence field, expand one prompt, and answer one scenario -> there is no page-level horizontal overflow, navigation does not cover headings, and long labels or feedback do not overlap.

Test 6 [Unit] (Edge - keyboard and state): Use only Tab, Enter, and Space on all Snowflake and scenario controls -> focus is visible, exactly one Snowflake button reports `aria-pressed="true"`, the selected scenario option updates immediately, and feedback is announced through its live region.
