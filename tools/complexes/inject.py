"""Inject the 'Les nombres complexes' chapter into index.html (same method as tools/suites/inject.py, tools/trace/trace_build.py).

Usage:  python3 inject.py <base index.html (without the chapter)> <repo root> <cx_block.js> <assets dir>
Every patch is asserted to match exactly once, so nothing else in the page can change by accident.
"""
import re, sys, os, shutil
base, repo, blockjs, assets = sys.argv[1:5]
s = open(base, encoding='utf-8').read()
blk = open(blockjs, encoding='utf-8').read()
assert '\u2062' not in s   # the italic delimiter is unused by the existing page

# 1) data block, right after the ln chapter
m = re.search(r"CH\.push\(\{id:'ln'.*?tracks:\[[^\]]*\]\}\);\n", s, re.S); assert m
s = s[:m.end()] + blk.lstrip('\n') + s[m.end():]

# 2) chapter-picker button next to ln's
i0 = s.find("${CH.filter(c=>c.id==='ln'"); assert i0 > 0 and s.count("${CH.filter(c=>c.id==='ln'") == 1
i1 = s.index(".join('')}", i0) + len(".join('')}")
old = s[i0:i1]
assert old.count("'ln'") == 1 and old.count('data-v="ln"') == 1 and old.count("lnD") == 1
s = s.replace(old, old + old.replace("'ln'", "'complexes'").replace('data-v="ln"', 'data-v="complexes"').replace("lnD", "cxD"))

# 3) wide-lesson layout class (same as ln)
o = "||LS.chapter==='ln'?' lwder':''"
assert s.count(o) == 1
s = s.replace(o, "||LS.chapter==='ln'||LS.chapter==='complexes'?' lwder':''")

# 4) lesson body class (ln readability + our own spacing/accents)
o = "les.id.indexOf('ln-')===0?' rnb sub lnb':''"
assert s.count(o) == 1
s = s.replace(o, "les.id.indexOf('ln-')===0?' rnb sub lnb':les.id.indexOf('cx-')===0?' rnb sub lnb cxb':''")

# 5) two additive block kinds: per-language display math (xm) and callouts (cx), in lessons AND in corrections
o = "const blkHTML=(bs,c)=>(bs||[]).map(b=>b.dtab?dtabHTML(b.dtab):b.img?"
assert s.count(o) == 1
helpers = ("const cxHTML=b=>{const ps=b[lang]||b.fr;return `<aside class=\"cxq cxq-${b.k}\"${lang==='ar'?' lang=\"ar\" dir=\"rtl\"':''}>${ps.map(p=>p.startsWith('$$')?`<div class=\"lwm\" dir=\"ltr\">${KT(p.slice(2,-2),1)}</div>`:`<p>${rich(p)}</p>`).join('')}</aside>`};"
           "const xmHTML=(b,o)=>`<div class=\"lwm${o&&o.big?' lwbig':''}\" dir=\"ltr\">${KT(b[lang]||b.fr,1)}</div>`;\n")
s = s.replace(o, helpers + "const blkHTML=(bs,c)=>(bs||[]).map(b=>b.dtab?dtabHTML(b.dtab):b.cx?cxHTML(b.cx):b.xm?xmHTML(b.xm,b):b.img?")
o = "${s.dtab?dtabHTML(s.dtab):''}${s.img?imgHTML(s.img):''}</div>`).join('')}"
assert s.count(o) == 1
s = s.replace(o, "${s.dtab?dtabHTML(s.dtab):''}${s.cx?cxHTML(s.cx):''}${s.xm?xmHTML(s.xm,s):''}${s.img?imgHTML(s.img):''}</div>`).join('')}")

# 6) italics: U+2062 delimiters (the base page does not use that character; checked at the top)
o ="esc(p).replace(/\\n/g,'<br>')"
assert s.count(o) == 1
s = s.replace(o, o + ".replace(/\\u2062([^\\u2062]*)\\u2062/g,'<i>$1</i>')")

# 7) language-specific figure (pageab_fr / _en / _ar), same mechanism as ln's log_notation
o = "const trSrc=u=>u.replace("
assert s.count(o) == 1
s = s.replace(o, "const trSrc=u=>u.replace(/(assets\\/complexes\\/pageab)_(fr|en|ar)\\.png$/,'$1_'+lang+'.png').replace(")

# 8) CSS
css = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cx.css'), encoding='utf-8').read()
assert s.count('</head>') == 1
s = s.replace('</head>', '<style id="cxcss">\n' + css + '\n</style>\n</head>')

open(os.path.join(repo, 'index.html'), 'w', encoding='utf-8').write(s)

# 9) figures
dst = os.path.join(repo, 'assets', 'complexes'); os.makedirs(dst, exist_ok=True)
MAP = {'ensembles_de_nombres_cote': 'ensembles', 'plan_complexe_fond_blanc': 'plan_lt', 'plan_complexe_fond_noir': 'plan_dk',
       'complex_plane_points': 'points_lt', 'complex_plane_points_black': 'points_dk', 'line_diagram_white': 'line_lt', 'line_diagram_dark': 'line_dk',
       'circle_diagram_white': 'circle_lt', 'circle_diagram_dark': 'circle_dk', 'complex_plane_ABC_white': 'abc_lt', 'complex_plane_ABC_black': 'abc_dk',
       'complex_plane_argz_white': 'argz_lt', 'complex_plane_argz_black': 'argz_dk', 'pageabtexample1_fr': 'pageab_fr', 'pageabtexample1_en': 'pageab_en', 'pageabtexample1_ar': 'pageab_ar'}
for a, b in MAP.items(): shutil.copy(os.path.join(assets, a + '.png'), os.path.join(dst, b + '.png'))

# 10) light-theme figures ship with an opaque white background; the page is grey, so turn that white into real transparency
#     (colour un-mixing: alpha = 1 - min(r,g,b)/255, colour = (pixel - 255*(1-alpha)) / alpha  -> same look as multiply, on any page colour)
import numpy as np
from PIL import Image
for f in sorted(os.listdir(dst)):
    if not f.endswith('_lt.png'): continue
    im = np.asarray(Image.open(os.path.join(dst, f)).convert('RGBA')).astype(np.float64)
    rgb = im[..., :3]; a = 1.0 - rgb.min(axis=2) / 255.0
    safe = np.maximum(a, 1e-6)[..., None]
    col = np.clip((rgb - 255.0 * (1.0 - a[..., None])) / safe, 0, 255)
    col[a < 0.004] = 0
    out = np.dstack([col, (a * im[..., 3] / 255.0 * 255.0)[..., None]]).round().astype(np.uint8)
    Image.fromarray(out, 'RGBA').save(os.path.join(dst, f), optimize=True)
print('injected', len(s), 'figures', len(os.listdir(dst)))
