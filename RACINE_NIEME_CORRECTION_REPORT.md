# Racine n-ième — Original French exercise correction report

## 1. Files changed
- `index.html`: ONLY the Racine n-ième data block (RNEX exercises + ARX entries) was replaced. Verified byte-identical outside that block. RNLES (6 lessons / 12 steps) verified identical to v16.
- Added: `backup/index.before-racine-correction.html` (exact v16), `tools/racine-correction/` (extraction/build/test scripts, intermediate JSON), this report.
- Not touched: Continuité, landing page, auth/session, Supabase, SQL, other chapters.

## 2. Final count per tier
CHICK 10, CHICKEN 10, RAVEN 11, EAGLE 12, PHOENIX 3 = **46** (checked in the running app, FR/EN/AR).

## 3. Recovery
All 46 exercises and corrections recovered from `Racine_d_ordre_n.docx`. 520 math fragments in the exercise section; 509 appear verbatim in the data, the other 11 are the deliberate fixes in section 5.

## 4. Word equations needing special extraction
27 plain square roots (`<m:degHide>`, no index) are silently dropped by pandoc/text extraction. Recovered by patching the XML. Affected: CHICK-05/06, CHICKEN-09/10, RAVEN-09 (E2), RAVEN-11, PHOENIX-01 (√(1+2x)), PHOENIX-02 (√(x²+2x+3)), plus √2 in CHICK-06/CHICKEN-09 corrections and the e.g. √(…) in RAVEN-09 corrections.

## 5. Ambiguities / deliberate presentation fixes (math unchanged)
- Empty `lim` subscript in the source (Word equation was empty): CHICKEN-01, 02, 03, 05, RAVEN-05, EAGLE-06 corrections. Filled with the variable from the same exercise's statement (x→0, 1, −1, +∞, −∞, +∞).
- Typed jammed text inside equations split: RAVEN-05 ("avec"), RAVEN-07 (two equalities fused), EAGLE-01 (commas), EAGLE-06 ("0oub"), EAGLE-11 ("ou"), EAGLE-12 ("1etf").
- `R` typed in Word shown as ℝ.
- PHOENIX statements 2 and 3 are bare equations in the source ("1 Calculer / 2 / 3"); "Calculer :" added to all three.
- RAVEN corrections "10)1." and "2." were mapped to RAVEN-10 and RAVEN-11.
- Source note "les deux dernières questions sont très difficiles et pas au programme" sits between EAGLE-10 and EAGLE-11; interpreted as questions 11 and 12. **Please confirm.**
- Source correction labels (1), 2), 3)) for EAGLE-12 vs a, b, c in the statement kept as in the source.
- I checked the mathematics of every correction by hand; no errors found. Limits/results are as in the source.
- DOCX course part still has the original −3x application with the author remark; lessons were left as in v16 (they use the AI-ready −x version).

## 6. Translations
EN and AR complete for all 46 (statements and corrections). Math is injected programmatically from the French, so it is identical in all languages. Arabic not reviewed by a native speaker.

## 7. Notes retained
Kept (student-facing, reworded in clean French/EN/AR): EAGLE optional-tier note (EAGLE-01), trigonometry-outside-syllabus note (EAGLE-05), last-two-questions note (EAGLE-11, 12). Not shown: the internal "QUICK NOTE … DO NOT INTEGRATE IN OTHER LESSONS". The old v16 EAGLE warning block (from the English file) was removed; it is not in the DOCX.

## 8. Tests actually performed
Chromium/Playwright on a local copy, local KaTeX, **stubbed login/DB (not the real authenticated workspace)**: all 46 exercises × FR/EN/AR with correction shown: 539 KaTeX nodes per language, 0 KaTeX errors, no raw `$`/`\cmd`/`**`, no JS errors, no EN/FR text leaking into the wrong language; exact tier counts; Phoenix warning appears. Screenshots reviewed for a few exercises (AR RTL, PHOENIX table).

## 9. Not verified
Authenticated workspace and saved-session refresh; mobile layout of wide formulas (they scroll); every screen visually. Saved attempts keyed by old exercise ids (`rn-chick-01` …) would now point to different exercises.

## 10. Backup
`backup/index.before-racine-correction.html`
