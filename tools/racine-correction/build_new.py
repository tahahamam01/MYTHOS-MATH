import sys,re,json
sys.path.insert(0,'/home/claude/work/proj/mythos-math/tools/racine-nieme')
import parse
parse.U='/mnt/user-data/uploads/'
import build as B
B.FRF='Racine_d_ordre_n_AI_ready.md'
from tr import TR,NOTES,TABLE_HEAD,TABLE_ROWS
APOS=B.APOS
EX=json.load(open('/home/claude/work/fr_final.json',encoding='utf8'))
TIER={'CHICK':'ve','CHICKEN':'e','RAVEN':'m','EAGLE':'h','PHOENIX':'x'}
def fill(tpl,ms,where):
    used=[int(x) for x in re.findall(r'\{(\d+)\}',tpl)]
    assert sorted(used)==list(range(1,len(ms)+1)),(where,tpl,len(ms),used)
    return re.sub(r'\{(\d+)\}',lambda m:'$'+ms[int(m.group(1))-1]+'$',tpl)
def prefix(s): return ('• ' if s.startswith('• ') else '')+('**' if '**' in s else '')
ARX={}
def reg(en,ar):
    if en in ARX: assert ARX[en]==ar,(en,ARX[en],ar)
    ARX[en]=ar
def pair(tpl_fr,ms,en,ar,where):
    assert prefix(tpl_fr)==prefix(en)==prefix(ar),(where,tpl_fr,en,ar)
    f=fill(tpl_fr,ms,where);e=fill(en,ms,where);a=fill(ar,ms,where)
    return f,e,a
def fmt_fr(s): return s  # APOS only affects ASCII apostrophes in text; source already typographic
OUT=[];stats={}
for ex in EX:
    tier,n=ex['id'].split('-')
    eid='rn-%s-%s'%(tier.lower(),n)
    tr=iter(TR[ex['id']])
    def conv(it,where):
        if 'x' in it: return {'x':it['x']}
        if it['t'].startswith('<TABLE>'): return {'dtab':'TABLE'}
        en,ar=next(tr)
        f,e,a=pair(it['t'],it['m'],en,ar,where)
        reg(e,a)
        return {'fr':f,'en':e}
    st=[conv(it,ex['id']+' stmt') for it in ex['stmt']]
    sol=[conv(it,ex['id']+' sol') for it in ex['sol']]
    left=list(tr); assert not left,(ex['id'],'unused translations',len(left))
    first=st[0]
    if 'x' in first: p={'fr':'$'+first['x']+'$','en':'$'+first['x']+'$'}
    else: p=first
    blocks=[]
    for b in st[1:]:
        assert 'fr' in b,(ex['id'],b)
        blocks.append(b)
    note=None
    if ex['id']=='EAGLE-01': note='opt'
    if ex['id']=='EAGLE-05': note='trig'
    if ex['id'] in('EAGLE-11','EAGLE-12'): note='last2'
    if note:
        f,e,a=NOTES[note]; reg(e,a); blocks.append({'fr':f,'en':e})
    for i,s in enumerate(sol):
        if 'dtab' in s:
            rows_fr=[TABLE_HEAD['fr']]+TABLE_ROWS
            sol[i]={'dtab':{'fr':rows_fr,'en':[TABLE_HEAD['en']]+TABLE_ROWS,'ar':[TABLE_HEAD['ar']]+TABLE_ROWS}}
    e={'id':eid,'d':TIER[tier],'p':{'fr':p['fr'],'en':p['en']},'q':'','sol':sol}
    if blocks: e['blocks']=blocks
    OUT.append(e)
    stats[tier]=stats.get(tier,0)+1
print(stats,len(OUT))
# lessons (unchanged code path)
L=B.build_lessons()
lessons=[{'id':l['id'],'title':l['title'],'steps':l['steps']} for l in L]
ARXALL=dict(B.ARX); 
for k,v in ARX.items(): ARXALL[k]=v
ids=[e['id'] for e in OUT]
main=[i for i in ids if '-phoenix-' not in i]; opt=[i for i in ids if '-phoenix-' in i]
j=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
code=("\n/* ===== RACINE N-IÈME — PC / SM / SVT (lessons: Racine_d_ordre_n_AI_ready.md FR / Nth_root_course_EN.md / Nth_root_course_AR.md; exercises: the 46 ORIGINAL French exercises + corrections recovered from Racine_d_ordre_n.docx, incl. its Word equation objects, translated to EN/AR; same engine as Continuité) ===== */\n"
 "const RNLES="+j(lessons)+";\n"
 "const RNEX="+j(OUT)+";\n"
 "RNEX.forEach(e=>{e.ex=true;EXB[e.id]=e});\n"
 "Object.assign(ARX,"+j(ARXALL)+");\n"
 "T.fr.rnD=\"Définition, propriétés, simplification, équations et limites avec racines n-ièmes.\";T.en.rnD=\"Definition, properties, simplification, equations and limits with n-th roots.\";T.ar.rnD=\"التعريف، الخاصيات، التبسيط، المعادلات والنهايات التي تحتوي على جذور من الرتبة n.\";\n"
 "CH.push({id:'racine',kind:'lesson',dk:'rnD',title:[\"Racine n-ième\",\"Nth roots\",\"الجذر من الرتبة n\"],lessons:RNLES,exercises:"+j(main)+",optional:"+j(opt)+",tracks:['PC','SM','SVT']});\n")
open('/home/claude/work/rn_block_new.js','w',encoding='utf8').write(code)
json.dump(OUT,open('/home/claude/work/rnex_new.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
# regression: lessons identical to v16?
s=open('/home/claude/work/proj/mythos-math/backup/index.before-racine-correction.html',encoding='utf8').read()
m=re.search(r'const RNLES=(\[.*?\]);\nconst RNEX=',s,re.S)
old=json.loads(m.group(1))
print('lessons identical to v16:',old==lessons)
i0=s.index('const RNLES'); oa=re.search(r'Object\.assign\(ARX,(\{.*?\})\);\nT\.fr\.rnD',s[i0:],re.S)
oldarx=json.loads(oa.group(1))
lessonarx={k:v for k,v in B.ARX.items()}
miss=[k for k in lessonarx if oldarx.get(k)!=lessonarx[k]]
print('lesson ARX entries differing from v16:',len(miss))
