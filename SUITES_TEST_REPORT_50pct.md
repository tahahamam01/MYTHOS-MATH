# Les Suites — 50% report (browser testing)

Environment: headless Chromium (Playwright), KaTeX served locally, FR / EN / AR, desktop 1280 px and phone 390 px.

## Results
- Crawl: 366 lesson steps + 408 exercise pages (69 exercises x 3 languages x 2 widths, plus 53 steps) -> 0 KaTeX errors, 0 raw `$`, 0 `undefined/NaN`, 0 stray `[R#]` markers, 0 broken images, 0 JS page errors, 0 horizontal overflow.
- Applications: view correction -> "Tu as réussi ?" -> OUI -> "Bravo !" + RÉESSAYER; NON path present. Same behaviour as existing chapters. Checked FR and AR (RTL).
- Dominoes figure: black version in light theme, white version in dark theme; the other is hidden.
- Regression: 1,008 pages (landing, Basics, Dérivabilité, Branches, Continuité, Racine x FR/EN/AR) render byte-identical to backup/index.before-suites.html.
- index.html vs backup: one inserted data block + 4 single-line edits (CSS, chapter button, layout class, lesson-body class). JS syntax check passes.

## Fixes made at this stage
1. Chapter description line: removed raw `$u_{n+1}=f(u_n)$` (FR/EN/AR).
2. 16 italic spans (`*...*` containing math, in corrections of lessons 13 and 14 and 4 exercises) were showing literal asterisks -> now bold, as decided for italics.
3. Lesson 14, step 6: a very long inline formula pushed the phone page wider than the screen -> Suites-only CSS lets that paragraph scroll inside itself (class `sub`, Suites lessons only).

## Left as-is (for your decision)
- Lesson 5, step 2 (FR): "Exemple. Énoncé : ..." comes from the source text of a lesson example (not an application), so it was kept.
- Lesson 3 title "La Reccurence": the source's own notes say this typo is kept from the original.
- PHOENIX readings [R11], [R14], [R15] still need your confirmation.

## Not done yet (50% -> 100%)
Final read-through of PHOENIX, final ZIP + integrity check, final report.
