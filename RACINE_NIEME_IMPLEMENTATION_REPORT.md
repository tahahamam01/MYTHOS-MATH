# Racine n-ième — Implementation report

## Files changed
- `index.html` only: one data block inserted after the Continuité `CH.push(...)` (~7 lines), plus 2 one-line edits (chapter-picker button next to Continuité's; `lwder` layout class now also covers `racine`).
- Added: `backup/index.before-racine-nieme.html` (state just before this work), `tools/racine-nieme/` (generator + test scripts), this report.
- Continuité (`COLES`, `COEX`, `COAPPS`) verified identical to the backup. Landing page, auth, Supabase, logo, Phoenix assets untouched.

## Implemented
- Chapter `racine` ("Racine n-ième" / "Nth roots" / "الجذر من الرتبة n"), tracks PC, SM, SVT, same engine as Continuité.
- 6 lessons / 12 steps: Introduction & définition · Propriétés (table) · Simplification (+Applications 1, 2) · Identités & équations (+application) · Limites avec racines (+applications) · Notes.
- 45 exercises with corrections: CHICK 9, CHICKEN 9, RAVEN 9, EAGLE 9, PHOENIX 9 (optional, existing Phoenix warning screen). Tiers exactly as in the source.
- EAGLE-level warnings (source says specific to this lesson) shown inside EAGLE-01 only.
- Content is generated from the 3 source files by `tools/racine-nieme/build.py` and injected by `inject.py`.

## Tests actually run (Chromium/Playwright on a local copy; KaTeX from a local npm copy; stubbed login/DB — NOT the real authenticated workspace)
- Chapter card appears on the session home; chapter overview opens; 6 lessons listed; 36/36 non-Phoenix exercises counted.
- All 12 lesson steps x FR/EN/AR: 0 KaTeX errors, no raw `$`, `\command` or `**`.
- All 45 exercises with correction shown x FR/EN/AR: 0 errors; no English text leaking into Arabic.
- Arabic: `dir=rtl`; math spans are `direction:ltr; unicode-bidi:isolate`. No JS page errors.

## NOT verified / limitations
1. Real authenticated workspace not tested; refresh with a real saved Supabase session not tested (stub DB has no sessions).
2. No figures: the source files contain no images, so none were added or invented.
3. No mascots added in lessons; tier mascots appear automatically via the existing exercise system.
4. **French exercises are not in the French source** (`Racine_d_ordre_n_AI_ready_1.md` ends after section 6: no exercises, no Notes). French statements/corrections were derived from the English file by phrase substitution (math untouched); the FR Notes and EAGLE warning were written by hand. **Please proofread the FR exercises.**
5. FR editorial notes not shown to students: "(ajoutée)" in the odd-index remark, the "Énoncé corrigé pour 2 (−3x → −x)" line and the parenthetical about the original −3x. They are absent from the EN/AR files too.
6. Dark/light check was only done by screenshots on lessons (no figures involved); not every screen reviewed pixel by pixel.
7. Arabic comes from the supplied Arabic file; not re-reviewed by a native speaker.

## Next agent
`python3 tools/racine-nieme/build.py && python3 tools/racine-nieme/inject.py` (paths are absolute to the sandbox; adjust). Tests: `t5.py` (lessons), `t9.py` (exercises); they need `stub.js` and a local KaTeX.
