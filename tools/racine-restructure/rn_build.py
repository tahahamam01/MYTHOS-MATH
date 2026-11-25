# -*- coding: utf-8 -*-
import json, re, sys, shutil, os
sys.path.insert(0, '/home/claude/work')
import rn_p1, rn_p2, rn_p3, rn_p4
from rn_p1 import tt

ROOT = '/home/claude/proj/mythos-math/'
SRC = ROOT + 'backup/index.before-racine-restructure.html'
if not os.path.exists(SRC):
    shutil.copy(ROOT + 'index.html', SRC)          # keep the file we received as backup (only once)
h = open(SRC, encoding='utf8').read()
lines = h.split('\n')

def find(prefix):
    for i, l in enumerate(lines):
        if l.startswith(prefix): return i
    raise SystemExit('missing ' + prefix)

iL, iE, iC = find('const RNLES='), find('const RNEX='), find("CH.push({id:'racine'")
old_les = json.loads(lines[iL][len('const RNLES='):].rstrip(';'))

# ---- lessons
l2 = [l for l in old_les if l['id'] == 'rn-l2'][0]
l2['steps'][0]['t'] = tt("Propriétés", "Properties", "الخاصيات")
old_l5s1 = [l for l in old_les if l['id'] == 'rn-l5'][0]['steps'][0]
dtab = [b for b in old_l5s1['blocks'] if b.get('dtab')][0]
rn_p1.L5['steps'][0]['blocks'].append(dtab)
NEW_LES = [rn_p1.L1, l2, rn_p1.L3, rn_p1.L4, rn_p1.L5]
for l in NEW_LES:
    for s in l['steps']:
        s.setdefault('apps', []); s.setdefault('story', {"fr": "", "en": ""})

# ---- exercises: keep ids / order of the old list
old_ids = re.findall(r'"(rn-(?:chick|chicken|raven|eagle|phoenix)-\d+)"', lines[iC])
new_by_id = {e['id']: e for e in rn_p4.EX}
order = []
for i in old_ids:
    if i not in order: order.append(i)
assert order == [e['id'] for e in sorted(rn_p4.EX, key=lambda e: order.index(e['id']))], 'order'
assert set(order) == set(new_by_id), set(order) ^ set(new_by_id)
NEW_EX = [new_by_id[i] for i in order]
print('exercises', len(NEW_EX), 'apps', len(rn_p1.APPS), 'lessons', len(NEW_LES))

J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
lines[iL] = 'const RNLES=' + J(NEW_LES) + ';'
lines[iE] = 'const RNAPPS=' + J(rn_p1.APPS) + ';RNAPPS.forEach(a=>APPBANK[a.id]=a);\nconst RNEX=' + J(NEW_EX) + ';'
h = '\n'.join(lines)

def rep(old, new, count=1):
    global h
    assert h.count(old) >= 1, 'not found: ' + old[:80]
    if count == 1: assert h.count(old) == 1, ('not unique (%d): ' % h.count(old)) + old[:80]
    h = h.replace(old, new)

# ---- CSS
CSS = (".lwextra{border:2px dashed var(--ln);border-inline-start:5px solid #2b7bff;padding:14px 18px;margin:22px 0;background:var(--sf)}"
       ".lwextra .lwbadge{display:inline-block;font:800 11px var(--ui);letter-spacing:.1em;text-transform:uppercase;border:2px solid #2b7bff;padding:2px 10px;margin-bottom:6px}"
       ".lwextra .lwbadge:before{content:'ℹ ';}"
       ".phxw.egw{border-inline-start-color:#2b7bff}.dnote.egn{border-inline-start-color:#2b7bff;font-size:15px;margin:14px 0}"
       ".egw .egl{opacity:.85;font-size:14px;margin:12px 0 18px}"
       ".rnb .lwm{padding:8px 0;margin:8px 0}.rnb .lwstory{margin:14px 0}"
       ".lwa[data-k^=\"rn-\"] .lws p,.lwa[data-k^=\"ex:rn-\"] .lws p{margin:16px 0 4px}"
       ".lwa[data-k^=\"rn-\"] .lwm,.lwa[data-k^=\"ex:rn-\"] .lwm{padding:10px 0;margin:6px 0}"
       ".lwa[data-k^=\"rn-\"] .lwm .katex-display,.lwa[data-k^=\"ex:rn-\"] .lwm .katex-display{margin:.7em 0}"
       ".lwa[data-k^=\"rn-\"]>p,.lwa[data-k^=\"ex:rn-\"]>p{margin:10px 0}")
rep('.phxw{border:2px solid var(--ln)', CSS + '.phxw{border:2px solid var(--ln)')


# ---- lesson body: extra aside + spacing class
rep('<div class="lwbody" ${ar?', '<div class="lwbody${les.id.indexOf(\'rn-\')===0?\' rnb\':\'\'}" ${ar?')
rep("${s.note?`<aside class=\"dnote lwnote\">${prose(s.note)}</aside>`:''}",
    "${s.note?`<aside class=\"dnote lwnote\">${prose(s.note)}</aside>`:''}${s.extra?`<aside class=\"lwextra\"><span class=\"lwbadge\">${richT(s.extra.badge)}</span>${blkHTML(s.extra.blocks,'lwstory')}</aside>`:''}")

# ---- hide 'tu as reussi' when correction hidden (apps + exercises)
rep("${steps(app)}</div>`}${assessHTML(cur,les,s,app)}", "${steps(app)}</div>${assessHTML(cur,les,s,app)}`}")
rep("${steps(e)}</div>`}${assessHTML(cur,les,null,e)}", "${steps(e)}</div>${assessHTML(cur,les,null,e)}`}")

# ---- Eagle warning (blue) + exercise notes
EG = r"""const egAck=()=>{if(LS&&LS.egOk)return true;try{return localStorage.getItem('mm-eg-ok-racine')==='1'}catch(e){return false}};
const EGT={t:['Niveau Eagle : avant de commencer','Eagle level: before you start','مستوى النسر: قبل أن تبدأ'],
n:['**Note :** ces questions sont assez complexes ; cette leçon n’a pas grand-chose à présenter à part l’idée générale (limites, équations et simplifications). Le niveau Raven est suffisant, mais si vous voulez améliorer votre niveau encore plus et que votre amour et votre curiosité pour les mathématiques vous démangent, allez-y !','**Note:** these questions are fairly complex; this lesson has little to present beyond the general idea (limits, equations and simplifications). The Raven level is enough, but if you want to improve even further and your love and curiosity for mathematics are itching, go for it!'],
o:['Cette note n’apparaît que dans cette leçon.','This note only appears in this lesson.','تظهر هذه الملاحظة في هذا الدرس فقط.'],g:['Compris, commencer','Got it, start','فهمت، ابدأ']};
function egWarn(sw){const d=T[lang].dir,i=LI(),n=lang==='ar'?(AX(EGT.n[1])||EGT.n[1]):EGT.n[lang==='en'?1:0];return `<div class="lwstep ${sw}"><section class="phxw egw" role="region" lang="${lang}" dir="${d}">${exImg('h')}<h2 class="lwt2">${EGT.t[i]}</h2><p>${rich(n)}</p><p class="egl">${EGT.o[i]}</p><div class="lwrow"><button type="button" class="lwb" data-a="go-ex">${d==='rtl'?'›':'‹'} ${t('exBack')}</button><button type="button" class="lwb pri" data-a="egok">${EGT.g[i]}</button></div></section></div>`}
const exNote=e=>e.note?`<aside class="dnote egn" role="note">${rich(AX(e.note.en)||e.note[PL()])}</aside>`:'';
"""
rep("function exHTML(sw){", EG + "function exHTML(sw){")
rep("if(LS.lesson==='x'&&!phxAck())return phxWarn(sw);", "if(LS.lesson==='x'&&!phxAck())return phxWarn(sw);\n if(LS.lesson==='h'&&CHP().id==='racine'&&!egAck())return egWarn(sw);")
rep("</header>${e.p?`<p>", "</header>${e.top?exNote(e):''}${e.p?`<p>")
rep("${blkHTML(e.blocks)}`;\n if(!cur)h+=", "${blkHTML(e.blocks)}${e.top?'':exNote(e)}`;\n if(!cur)h+=")
rep("else if(a==='phxok'){", "else if(a==='egok'){try{localStorage.setItem('mm-eg-ok-racine','1')}catch(e){}LS.egOk=true;rw()}  else if(a==='phxok'){")

# ---- CH.push: nothing to change (same exercise ids); lessons = RNLES
open(ROOT+'index.html','w',encoding='utf8').write(h)
print('written', len(h))
