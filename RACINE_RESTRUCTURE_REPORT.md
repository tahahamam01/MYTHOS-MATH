# Racine n-ième — restructure report
Backup of the received file: backup/index.before-racine-restructure.html
Build scripts: /tools/racine-restructure (rn_p1..p4.py, rn_build.py)

## Fixed (numbers = your list)
1 Title: removed the KaTeX n (gap) -> plain "n-ièmes"; step numbers removed like other chapters.
2 Remarque: "bijective" removed, rest kept.
3/9 Applications now use the same system as other chapters (APPBANK cards: "Application N", "Voir la correction", "Tu as réussi ?"); no "Énoncé". Limits apps have "Calculer la limite :".
4/6/7/11/12/13/17 Spacing: every equation on its own line, aligned lists for statements, extra CSS spacing (Racine only). Identities one per line. Limits lesson cut into 3 pages (retenir / étapes / exemple).
5/10 Removed the invented "Notes à retenir" lesson (not in your docx) -> no extra "Leçon suivante".
8 Hors programme is now a separate framed "i" aside.
11 "Écrire plus simplement" -> "Simplifier".
14/16 Every limit: "Calculer la limite", step 1 substitution, and "forme indéterminée" always written.
15/20 Eagle: blue-line warning screen (like Phoenix) with your full note + "only in this lesson" line. Trig note on Eagle 5 only; the 11-12 note shown at the top of both 11 and 12.
18 Hiding the correction now also hides "Tu as réussi ?" (shared code, all chapters).
19 Eagle 12: "Branche parabolique." is now a title of the statement, questions 1) 2) 3).
21 Phoenix 1: every coefficient computed and explained.

## Still to do / honest limits
- Arabic: new/restructured text lines have no Arabic yet (they fall back to French). Math is identical.
- Some very long equations (Eagle/Phoenix) still scroll sideways on narrow screens.
- Tested in Chromium with stubbed login: 46 exercises + 5 lessons, 0 KaTeX errors. Not tested on real account/phone.
- Eagle-9 etc.: sub-questions labelled 1) 2) consistently (docx mixed a,b,c / 1,2).
- Saved attempts on old exercise ids keep the same ids.
