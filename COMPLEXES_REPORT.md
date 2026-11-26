# Les nombres complexes — implementation report

New chapter `complexes` (button "Les nombres complexes" in the chapter chooser), in **FR / EN / AR**, each built from its own source file. No content was changed; no other lesson was touched.

## What was added
- **8 lessons / 30 steps**: Introduction, Définition, Forme algébrique, Module, Équations dans ℂ, Représentation géométrique, Les transformations usuelles, Toutes les règles.
- **16 applications** (statement + hidden correction, same card as the other chapters).
- **60 exercises** in the 5 tiers (Chick 10, Chicken 17, Raven 17, Eagle 15, Phoenix 1 — optional, behind the usual warning screen).
- **8 figures** (`assets/complexes/`): light/dark pairs switch with the theme; `pageab_fr|en|ar.png` follows the language.
- All math is real KaTeX (13,925 TeX strings, 0 errors in FR/EN/AR). 54 display equations contain words (`\text{et}` / `and` / `و`), so they are stored per language.
- Layout: ln-style readable type, generous spacing, accent colour on labels (yellow in dark, red in light — the site's own `--y`), boxed definition formulas, colour-coded callouts (Astuce / Note / Important), tables with math, true italics.
- Display equations wider than the column are shrunk just enough to fit (floor 50% on desktop, 62% on phones; beyond that they scroll inside their box).

## Source observations (nothing changed — flagged only)
- The three files were parallel block for block (2,875 blocks each); no reconciliation was needed.
- One display equation sat inside the "Astuce / Tip" blockquote; it is now rendered as display math inside the callout.
- Figures are placed by their exact position in the source (e.g. the U, N, K plane after the example; the A–H plane inside the correction).

## Existing code touched (7 lines, all additive; verified)
| Where | Change |
|---|---|
| chapter chooser | button for `complexes` next to ln's |
| `lwder` layout condition | also applies to `complexes` |
| lesson body class | `cx-` lessons get `rnb sub lnb cxb` |
| `blkHTML`, `steps` | two new block kinds: `xm` (per-language display math) and `cx` (callout) |
| `rich` | italic delimiter U+2062 (unused elsewhere) → `<i>` |
| `trSrc` | language-specific `pageab` figure |
| `<style id="cxcss">` | chapter CSS (all selectors scoped to `cx-` ids) |

## Verification
- Full crawl, 3 languages × light/dark × desktop (1280) and phone (390): every lesson step, application correction and exercise — 0 page errors, 0 KaTeX errors, 0 raw `$`, 0 stray `*`, 0 broken images, 0 horizontal page overflow.
- Regression: 522 pages of the other chapters (FR/EN/AR) hashed before/after — identical; the only difference is the new card in the chapter chooser.

## Rebuild
`tools/complexes/`: `parse.py` (md → blocks), `build.py` (→ data block), `inject.py` (patches `index.html`), `cx.css`, `fit.js`, `katexcheck.js`, `make_test.py` + `tests/` (crawler, regression).
