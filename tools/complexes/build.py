"""Les nombres complexes -> data block for index.html (FR / EN / AR, each from its own source md).

Output: <OUT>/cx_block.js  (JS to splice into index.html)  and  <OUT>/cx_math.json (every TeX string, for the KaTeX check).
Same engine / data model as Suites, Tracé and ln (lessons -> steps -> blocks, applications, exercises).
"""
import re, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse import parse

OUT = os.environ.get('CX_OUT', '/tmp/claude-0/-home-claude/1172a3da-d14e-52ac-ae2c-05145723c309/scratchpad/')
LG = ('fr', 'en', 'ar')
W = {l: parse(l) for l in LG}
F, E, A = W['fr'], W['en'], W['ar']
N = len(E)

# ---------------------------------------------------------------- alignment checks (the 3 files must be parallel)
for i in range(N):
    assert F[i][0] == E[i][0] == A[i][0], (i, F[i][:2], E[i][:2], A[i][:2])
    if E[i][0] in 'HL':
        assert F[i][1] == E[i][1] == A[i][1], (i, 'level')
    if E[i][0] == 'L':
        assert (F[i][2][0] == '-') == (E[i][2][0] == '-') == (A[i][2][0] == '-'), (i, 'list marker')
    if E[i][0] == 'T':
        assert len(F[i][2]) == len(E[i][2]) == len(A[i][2]) and all(len(a) == len(b) == len(c) for a, b, c in zip(F[i][2], E[i][2], A[i][2])), (i, 'table')
    if E[i][0] == 'Q':
        assert len(F[i][2]) == len(E[i][2]) == len(A[i][2]), (i, 'quote')

IT = '⁢'          # invisible separator: italic delimiter understood by the patched rich()
REPORT = {'leadin': [], 'big': 0, 'labels': 0}

# ---------------------------------------------------------------- text cleaning
def italics(s):
    """*x* -> IT x IT, each text run of an italic span wrapped separately so TeX inside stays upright-math."""
    maths = []
    def mask(m):
        maths.append(m.group(0)); return '\x01%d\x01' % (len(maths) - 1)
    t = re.sub(r'\$[^$]*\$', mask, s)
    def ital(m):
        inner = m.group(1)
        parts = re.split(r'(\x01\d+\x01)', inner)
        return ''.join(p if (p.startswith('\x01') or not p.strip()) else IT + p + IT for p in parts)
    t = re.sub(r'(?<![*\x01\w])\*(?!\*)([^*]+?)(?<!\*)\*(?![*\w])', ital, t)
    return re.sub(r'\x01(\d+)\x01', lambda m: maths[int(m.group(1))], t)

def cl(s):
    return italics(s.replace('`', '')).strip()

# ---------------------------------------------------------------- item builders
def text3(idx, prefix=('', '', ''), strip=None):
    raw = [W[l][idx][2] for l in LG]
    if strip: raw = [strip(r) for r in raw]
    return {'fr': prefix[0] + cl(raw[0]), 'en': prefix[1] + cl(raw[1]), 'ar': prefix[2] + cl(raw[2])}

def math_item(idx, big=False):
    tex = [W[l][idx][2].strip() for l in LG]
    if len(set(tex)) == 1:
        d = {'x': tex[0]}
    else:
        d = {'xm': {'fr': tex[0], 'en': tex[1], 'ar': tex[2]}}
    if big: d['big'] = 1
    return d

LABEL_KIND = [(r'^\*\*(Astuce|Tip)', 'tip'), (r'^\*\*(Remarque|Note)', 'note'), (r'^\*\*(Important|Attention|Warning)', 'imp')]
def callout(idx):
    ps = {l: [x if x.startswith('$$') else cl(x) for x in W[l][idx][2]] for l in LG}
    kind = 'note'
    for rx, k in LABEL_KIND:
        if re.match(rx, W['en'][idx][2][0]): kind = k
    return {'cx': {'k': kind, 'fr': ps['fr'], 'en': ps['en'], 'ar': ps['ar']}}

RH = {'Form', 'Notion', 'Case', 'Property', 'Transformation', 'Situation', ''}
def table_item(idx):
    rows = {l: [[cl(c) for c in r] for r in W[l][idx][2]] for l in LG}
    d = {'fr': rows['fr'], 'en': rows['en'], 'ar': rows['ar']}
    first = re.sub(r'\*', '', W['en'][idx][2][0][0]).strip()
    d['rh'] = 1 if (first in RH or first.startswith('$\\theta')) else 0
    if not d['rh']: del d['rh']
    return {'dtab': d}

IMAGES = {   # marker order -> (key, caption fr/en/ar)
    0: ('ensembles', "Les ensembles de nombres : $\\mathbb{N} \\subset \\mathbb{Z} \\subset \\mathbb{D} \\subset \\mathbb{Q} \\subset \\mathbb{R} \\subset \\mathbb{C}$",
        "The sets of numbers: N, Z, D, Q, R, C, each inside the next", "مجموعات الأعداد: كل مجموعة محتواة في التي تليها"),
    1: ('plan', "Les points $U$, $N$ et $K$ dans le plan complexe", "The points U, N and K in the complex plane", "النقط U و N و K في المستوى العقدي"),
    2: ('points', "Les points $A$, $B$, $C$, $D'$, $D$, $E$, $F$, $G$, $H$ dans le plan complexe", "The points A, B, C, D', D, E, F, G, H in the complex plane", "النقط A و B و C و D' و D و E و F و G و H في المستوى العقدي"),
    3: ('line', "Une droite $(D)$ du plan", "A line (D) of the plane", "مستقيم (D) في المستوى"),
    4: ('circle', "Un cercle de centre $\\Omega$ et de rayon $r$", "A circle with center Omega and radius r", "دائرة مركزها Ω وشعاعها r"),
    5: ('abc', "Les points $A$, $B$ et $C$ dans le plan complexe", "The points A, B and C in the complex plane", "النقط A و B و C في المستوى العقدي"),
    6: ('argz', "L'argument de $z$ : l'angle entre l'axe des réels et $(OA)$", "The argument of z: the angle between the real axis and (OA)", "عمدة z: الزاوية بين محور الأعداد الحقيقية و (OA)"),
    7: ('pageab', "Exemple : arguments de $z_1, \\dots, z_6$ lus sur le plan complexe", "Example: arguments of z1, ..., z6 read on the complex plane", "مثال: عمدة الأعداد z1 ... z6 على المستوى العقدي"),
}
ARX = {}
MARK = '⁠'
def reg(en, ar):
    k = en + MARK
    while k in ARX and ARX[k] != ar: k += MARK
    ARX[k] = ar; return k
IMGSEQ = [0]
MARK_IDX = [i for i, c in enumerate(E) if c[0] == 'IMG']   # position of each marker in the source = which figure it is
assert len(MARK_IDX) == len(IMAGES)
def image_items(idx):
    n = MARK_IDX.index(idx); IMGSEQ[0] += 1
    key, fr, en, ar = IMAGES[n]
    cap = lambda src: {'img': {'src': src, 'fr': fr, 'en': reg(en, ar)}}
    if key == 'ensembles': return [cap('assets/complexes/ensembles.png')]
    if key == 'pageab': return [cap('assets/complexes/pageab_fr.png')]
    return [cap('assets/complexes/%s_lt.png' % key), cap('assets/complexes/%s_dk.png' % key)]

def conv(idxs, lesson=False):
    """block indices -> list of items. lesson=True: definition formulas are boxed."""
    out = []; prev = None; pend_def = False
    for idx in idxs:
        k = E[idx][0]
        if k == 'P':
            out.append(text3(idx))
            pend_def = bool(re.match(r'\*\*(Definition|Définition)\b', E[idx][2]) or re.match(r'\*\*Définition|\*\*تعريف', F[idx][2]) or re.match(r'\*\*تعريف', A[idx][2]))
        elif k == 'M':
            big = lesson and pend_def
            if big: REPORT['big'] += 1
            out.append(math_item(idx, big)); pend_def = False
        elif k == 'L':
            mk, lvl = E[idx][2][0], E[idx][1]
            ind = ' ' * 2 * lvl
            if mk == '-':
                pf = (ind + ('• ' if lvl == 0 else '– '),) * 3
            else:
                pf = tuple(ind + W[l][idx][2][0] + ' ' for l in LG)
            out.append({l: pf[n] + cl(W[l][idx][2][1]) for n, l in enumerate(LG)}); pend_def = False
        elif k == 'T': out.append(table_item(idx)); pend_def = False
        elif k == 'Q': out.append(callout(idx)); pend_def = False
        elif k == 'IMG': out += image_items(idx); pend_def = False
        elif k == 'H': raise Exception(('unexpected heading in body', idx, E[idx]))
        else: raise Exception(k)
    return out

H = lambda i: [cl(W[l][i][2]) for l in LG]
is_app = lambda i: E[i][0] == 'H' and E[i][1] == 4 and E[i][2].startswith('Application')
is_cor = lambda i: E[i][0] == 'H' and E[i][1] == 4 and E[i][2].startswith('Correction')

# ---------------------------------------------------------------- lessons
ex_start = [i for i, c in enumerate(E) if c[0] == 'H' and c[1] == 2 and c[2].lower().startswith('exercise')][0]
lessons = []
for i in range(1, ex_start):
    c = E[i]
    if c[0] == 'H' and c[1] == 2: lessons.append({'title': H(i), 'steps': [], 'pre': []})
    elif c[0] == 'H' and c[1] == 3: lessons[-1]['steps'].append({'t': H(i), 'raw': []})
    else:
        L_ = lessons[-1]
        (L_['steps'][-1]['raw'] if L_['steps'] else L_['pre']).append(i)
for L_ in lessons:
    if L_['pre']:
        L_['steps'].insert(0, {'t': L_['title'], 'raw': L_['pre']})

def split_pair(items):
    """first text item -> p ; the rest -> blocks"""
    if items and 'fr' in items[0] and 'en' in items[0] and 'x' not in items[0]:
        return items[0], items[1:]
    return None, items

APPS = []
def make_app(stm, corrs):
    p, blocks = split_pair(conv(stm))
    sol = []
    for lab, body in corrs:
        if lab is not None and len(corrs) > 1:
            sol.append({l: '**' + cl(W[l][lab][2]) + '**' for l in LG})
        sol += conv(body)
    d = {'id': 'cx-app%d' % (len(APPS) + 1), 'own': True}
    if p: d['p'] = p
    d['q'] = ''
    d['blocks'] = blocks; d['sol'] = sol
    APPS.append(d); return d['id']

def process(raw):
    """-> list of sub-steps {'blocks': items, 'apps': [ids]}"""
    subs = [{'idx': [], 'apps': []}]
    i = 0
    while i < len(raw):
        k = raw[i]
        if is_app(k):
            j = i + 1; stm = []
            while not is_cor(raw[j]): stm.append(raw[j]); j += 1
            corrs = []
            while j < len(raw) and is_cor(raw[j]):
                lab = raw[j]; j += 1; body = []
                while j < len(raw) and E[raw[j]][0] != 'H': body.append(raw[j]); j += 1
                corrs.append([lab, body])
            lead = []
            if j < len(raw) and is_app(raw[j]):
                last = corrs[-1][1]
                if last and E[last[-1]][0] == 'P' and re.search(r':\s*$', E[last[-1]][2]):
                    lead = [last.pop()]; REPORT['leadin'].append((last and lead[0], E[lead[0]][2][:90]))
            subs[-1]['apps'].append(make_app(stm, corrs))
            if lead:
                subs.append({'idx': lead, 'apps': []})
            i = j
        else:
            if subs[-1]['apps']: subs.append({'idx': [], 'apps': []})
            subs[-1]['idx'].append(k); i += 1
    return subs

CONT = ('(suite)', '(continued)', '(تابع)')
LES = []
for n, L_ in enumerate(lessons, 1):
    steps = []
    for st in L_['steps']:
        subs = process(st['raw'])
        for si, sb in enumerate(subs):
            t = st['t'] if si == 0 else [st['t'][x] + ' ' + CONT[x] for x in range(3)]
            steps.append({'t': t, 'blocks': conv(sb['idx'], lesson=True), 'apps': sb['apps']})
    for k, st in enumerate(steps, 1): st['id'] = 's%d' % k
    LES.append({'id': 'cx-l%d' % n, 'title': L_['title'], 'steps': [{'id': s['id'], 't': s['t'], 'story': {'fr': '', 'en': ''}, 'blocks': s['blocks'], 'apps': s['apps']} for s in steps]})

# ---------------------------------------------------------------- exercises
TIER = [('CHICK', 've'), ('CHICKEN', 'e'), ('RAVEN', 'm'), ('EAGLE', 'h'), ('PHOENIX', 'x')]
EXS = []; cur_tier = None; cur = None; cnt = {}
for i in range(ex_start + 1, N):
    c = E[i]
    if c[0] == 'H' and c[1] == 3:
        m = re.search(r'(CHICKEN|CHICK|RAVEN|EAGLE|PHOENIX)\s*$', c[2]); assert m, c
        cur_tier = m.group(1); cnt[cur_tier] = 0; cur = None
    elif c[0] == 'H' and c[1] == 4:
        cnt[cur_tier] += 1
        cur = {'tier': cur_tier, 'n': cnt[cur_tier], 'st': [], 'sol': [], 'in': 'st'}; EXS.append(cur)
    elif c[0] == 'H' and c[1] == 5:
        assert c[2].startswith('Correction'); cur['in'] = 'sol'
    else:
        cur[cur['in']].append(i)
d_of = dict(TIER)
EXOUT = []
for e in EXS:
    p, blocks = split_pair(conv(e['st']))
    d = {'id': 'cx-%s-%02d' % (e['tier'].lower(), e['n']), 'd': d_of[e['tier']]}
    if p: d['p'] = p
    d['q'] = ''
    if blocks: d['blocks'] = blocks
    d['sol'] = conv(e['sol'])
    EXOUT.append(d)

# ---------------------------------------------------------------- finalise
j = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
main = [e['id'] for e in EXOUT if '-phoenix-' not in e['id']]
opt = [e['id'] for e in EXOUT if '-phoenix-' in e['id']]
DESC = {
 'fr': "Forme algébrique, conjugué et module, équations dans ℂ, représentation géométrique, argument, forme trigonométrique et exponentielle, transformations, puis des exercices du plus simple au plus difficile.",
 'en': "Algebraic form, conjugate and modulus, equations in ℂ, geometric representation, argument, trigonometric and exponential form, transformations, then exercises from easiest to hardest.",
 'ar': "الشكل الجبري، المرافق والمعيار، المعادلات في ℂ، التمثيل الهندسي، العمدة، الشكل المثلثي والشكل الأسي، التحويلات، ثم تمارين من الأسهل إلى الأصعب.",
}
code = ("\n/* ===== LES NOMBRES COMPLEXES — PC / SM / SVT (content from Les_nombres_complexes.md / Complex_numbers_EN_full.md / Les_nombres_complexes_AR_final.md; same engine as Suites / ln) ===== */\n"
        "const CXLES=" + j(LES) + ";\n"
        "const CXAPPS=" + j(APPS) + ";CXAPPS.forEach(a=>APPBANK[a.id]=a);\n"
        "const CXEX=" + j(EXOUT) + ";\nCXEX.forEach(e=>{e.ex=true;EXB[e.id]=e});\n"
        "Object.assign(ARX," + j(ARX) + ");\n"
        + ''.join("T.%s.cxD=%s;" % (l, j(DESC[l])) for l in LG) + "\n"
        + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fit.js"), encoding="utf-8").read().replace("\n", "") + "\n"
        "CH.push({id:'complexes',kind:'lesson',dk:'cxD',title:[\"Les nombres complexes\",\"Complex numbers\",\"الأعداد العقدية\"],lessons:CXLES,exercises:" + j(main) + ",optional:" + j(opt) + ",tracks:['PC','SM','SVT']});\n")
os.makedirs(OUT, exist_ok=True)
open(OUT + 'cx_block.js', 'w', encoding='utf-8').write(code)

# every TeX string, for the KaTeX check
maths = []
def walk(o, where):
    if isinstance(o, dict):
        if 'x' in o: maths.append((where, o['x']))
        if 'xm' in o: [maths.append((where + ':' + l, o['xm'][l])) for l in LG]
        for k, v in o.items():
            if k in ('fr', 'en', 'ar') and isinstance(v, str):
                for m in re.finditer(r'\$([^$]+)\$', v): maths.append((where + ':' + k, m.group(1)))
            elif k in ('fr', 'en', 'ar') and isinstance(v, list):
                for r in v:
                    if isinstance(r, str) and r.startswith('$$'): maths.append((where + ':' + k, r[2:-2])); continue
                    for c in (r if isinstance(r, list) else [r]):
                        for cc in (c if isinstance(c, list) else [c]):
                            for m in re.finditer(r'\$([^$]+)\$', cc): maths.append((where + ':' + k, m.group(1)))
            elif k not in ('x', 'xm'): walk(v, where)
    elif isinstance(o, list):
        for v in o: walk(v, where)
for L_ in LES: walk(L_, L_['id'])
walk(APPS, 'apps'); walk(EXOUT, 'ex')
json.dump(maths, open(OUT + 'cx_math.json', 'w', encoding='utf-8'), ensure_ascii=False)

print('lessons', len(LES), [len(l['steps']) for l in LES], file=sys.stderr)
print('apps', len(APPS), 'exercises', len(EXOUT), {t: sum(1 for e in EXOUT if e['d'] == t) for _, t in TIER}, file=sys.stderr)
print('images used', IMGSEQ[0], 'tex strings', len(maths), 'block bytes', len(code), file=sys.stderr)
print('boxed definition formulas', REPORT['big'], file=sys.stderr)
print('lead-ins moved out of corrections:', file=sys.stderr)
for x in REPORT['leadin']: print('  ', x[1], file=sys.stderr)
