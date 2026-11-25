# MYTHOS MATH — Continuité repair (handoff report)

Backup of the pre-repair file: `backup/index.before-continuite-repair.html` (byte-identical copy of the uploaded index.html).
Re-runnable pipeline (always rebuilds from that backup): `tools/continuite-repair/repair.py` (paths inside point to /home/claude/...; adjust).

## Files changed
- `index.html` only (plus new backup + this report + tools/). Three kinds of edits:
  1. CSS: the `.coimg` rule (one line, ~line 269) replaced by a themed "plate" block (12 lines).
  2. JS: `imgHTML` now adds class `co-dk` (fig1_tvi, dark-source artwork) or `co-lt` (others).
  3. Data: the `COAPPS`, `COLES`, `COEX` lines only (JSON arrays, same structure/ids/order, round-trip checked).
- No other line of index.html differs (verified by line diff). Landing page, auth, Supabase, assets, ARX translation table untouched.

## Done
1. Math typography: all plain-text/Unicode math in CHICK, CHICKEN, RAVEN, lesson "Lecture d'une courbe", TVI, Dichotomie and the applications converted to KaTeX `$…$` (fr + en; dtab cells incl. ar). Done by a rule-based converter + a short list of explicit overrides (build_data.py `PRE`). All 5,255 math fragments in the final data parse with KaTeX strict mode (1 pre-existing Arabic `\text{}` fragment in strict mode only; the site renders with strict:false).
   - A `C_{f}` (same form as Définition/EAGLE), B `f'(a)=\dfrac{y_{B}-y_{A}}{x_{B}-x_{A}}`, D four symmetry formulas, E `f''`, F extremums example: all wrapped.
   - C limits: parabolic-branch lines now `\lim_{x\to+\infty}\dfrac{f(x)}{x}=a` etc. For the three asymptote lines whose sentence already says "quand x tend vers …" the words were kept and `\lim` has no subscript (to avoid duplicating/rewording).
   - EAGLE and PHOENIX math untouched (entries differ from original only in the title/heading fields below).
2. Figures (CSS only, original PNGs, no redraw): themed plate (opaque #151515 dark / #c6c7c0 light), border via existing `--ln`; white-background art uses `multiply` (light) / invert+hue-rotate+`screen` (dark); the dark TVI art is inverted in light mode; 3 px clip removes a 1–2 px white edge artefact baked into fig1_tvi.png.
   - "First figure" (fig2_resolution_graphique) moved after the "Exemple. Pour résoudre f(x) = −1 …" paragraph (its "Figure :" caption follows it). fig4_exemple_complet not moved. fig3_application and fig1_tvi not moved.
3. CHICK 01–10: statements reconstructed from corrections (p, plus numbered `blocks` for chick-10). Corrections untouched. See list below.
4. EAGLE 15 title: « Le problème de synthèse » (en: "The synthesis problem"). Other titles already fine.
5. PHOENIX: « itérée » removed (en "Iterating" removed too, for consistency); disclaimer kept. Part B « Dénombrement des solutions » (en "Counting the solutions"); Part C unchanged; Part D « Solutions de l’équation $f^{2}(x)=x$ » (en "Solutions of the equation …").

## CHICK reconstructions (all 10 done; confidence)
01 dichotomy of x²−3 on [1;2], width 0.25 (medium: α given as positive root in [1;2]) · 02 inverse of x+3 · 03 inverse of 3x−2 · 04 inverse of x²+1 on [0;+∞[ · 05 inverse of x³−1 + check · 06 TVI x²=5 on [2;3] · 07 unique solution x³+2x=4 · 08 unique solution √x+x=4 on [1;4] · 09 unique solution x²+x=7 · 10 f=x³+x: continuity/monotony, f(x)=3 unique α in [1;2], dichotomy 0.25, inverse + curves. Please have a teacher skim them; none was flagged unreconstructable.

## Tests actually performed
- JSON round-trip of the three data arrays; all inline scripts parse (`new Function`).
- KaTeX strict validation of every `$…$` in the final data (node, katex 0.16 from local install).
- Content-preservation check: prose words (≥4 letters) outside math identical old vs new for CHICKEN/RAVEN/EAGLE/lessons/apps; only intended differences in CHICK/PHOENIX.
- Browser (Chromium/Playwright) harness using the site's real CSS + KaTeX: figures + sample formulas, dark and light, screenshots inspected; no horizontal overflow, no console errors.
- Landing page loads with no console errors in dark/light × fr/en/ar (Supabase stubbed, CDN KaTeX served locally).

## NOT verified
- The learning workspace itself (auth/Supabase-gated) was not opened in a browser; rendering there was checked via the harness with the same CSS/KaTeX, not in-app. Arabic/RTL workspace not visually checked (Continuité text falls back to fr/en in Arabic UI, as before).
- fig3_application.png is only 520×512 in the supplied files; no higher-resolution original exists in the ZIP/backups, so its resolution could not be improved (it is displayed at native size, capped at 520 px). Provide the original/vector file to fix this.
- Baked-in text inside fig2/fig4 (e.g. "même fonction f(x) = …" footer) remains part of the PNGs. fig3 labels "(5,0)" sits at x=6 in the artwork — pre-existing, untouched.
- Mapping assumption: "first/second/third/TVI figure" = fig2_resolution_graphique / fig4_exemple_complet / fig3_application / fig1_tvi.
