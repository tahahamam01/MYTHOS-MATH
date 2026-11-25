import re,json,shutil,os,sys
sys.path.insert(0,'/home/claude/w/tools')
from trace_parse import parse
P='/home/claude/w/m19/mythos-math/'
LG=('fr','en','ar')
D={l:parse(l) for l in LG}
N=len(D['en'])
for i in range(N): assert D['fr'][i][0]==D['en'][i][0]==D['ar'][i][0],i
FIG=json.load(open('/home/claude/w/spec/tracage_spec/figures.json'))['figures']
capfr={f['id']:f['title_fr'] for f in FIG}
EN={'F01':'Vertical asymptote: the curve runs along the wall without ever touching it','F02':'Horizontal asymptote: a floor or a ceiling','F03':'Oblique asymptote: f(x) = x + 1 + 1/x and the line (D): y = x + 1','F04':'Case 1: lim f(x)/x = 0, direction (Ox) — f(x) = √x','F05':'Case 2: lim f(x)/x = ±∞, direction (Oy) — f(x) = x² and eˣ','F06':'Case 3: lim f(x)/x = a ≠ 0 and lim [f(x) − ax] = ±∞, direction y = ax — f(x) = 2x + √x','F07':'Graphing f(x) = x − ln(x) step by step (5 cumulative frames)','F08':'Forbidden value: what the double bar ‖ gives on the curve','F09':'Do not confuse variation and sign','F10':'Convex ∪ (bowl) and concave ∩ (bell)','F11':'Inflection point: always draw the tangent — g(x) = x³ − 3x','F12':'Relative position: the line and the curve','F13':'Relative position of two curves: f(x) = x³ and g(x) = x','F14':'Parity: draw one half, then complete (examples x², x³ − 3x, 1/(x²−1))','F15':'Axis of symmetry x = 1: (x ; y) gives (2·1 − x ; y) — example h(x) = (x − 1)²','F16':'Center of symmetry Ω(1 ; 2): (x ; y) gives (2·1 − x ; 2·2 − y)','F17':'f(x) = 1/x: center O, the asymptotes x = 0 and y = 0 are preserved','F18':'Inverse: f(x) = eˣ and f⁻¹(x) = ln(x), mirror y = x','F19':'Inverse: horizontal tangent ↔ vertical tangent — f(x) = (x − 1)³ + 1'}
AR={'F01':'المقارب العمودي: المنحنى يسير بمحاذاة الجدار دون أن يلمسه أبدًا','F02':'المقارب الأفقي: أرضية أو سقف','F03':'المقارب المائل: f(x) = x + 1 + 1/x والمستقيم (D) : y = x + 1','F04':'الحالة 1: lim f(x)/x = 0، الاتجاه (Ox) — f(x) = √x','F05':'الحالة 2: lim f(x)/x = ±∞، الاتجاه (Oy) — f(x) = x² و eˣ','F06':'الحالة 3: lim f(x)/x = a ≠ 0 و lim [f(x) − ax] = ±∞، الاتجاه y = ax — f(x) = 2x + √x','F07':'رسم f(x) = x − ln(x) خطوة بخطوة (5 صور متتابعة)','F08':'القيمة الممنوعة: ماذا يعطي الخط المزدوج ‖ على المنحنى','F09':'لا تخلط بين التغيرات والإشارة','F10':'محدّب ∪ (وعاء) ومقعّر ∩ (جرس)','F11':'نقطة الانعطاف: ارسم دائمًا المماس — g(x) = x³ − 3x','F12':'الوضع النسبي: المستقيم والمنحنى','F13':'الوضع النسبي لمنحنيين: f(x) = x³ و g(x) = x','F14':'الزوجية: نرسم نصفًا ثم نُكمل (أمثلة x² و x³ − 3x و 1/(x²−1))','F15':'محور التماثل x = 1: (x ; y) يعطي (2·1 − x ; y) — المثال h(x) = (x − 1)²','F16':'مركز التماثل Ω(1 ; 2): (x ; y) يعطي (2·1 − x ; 2·2 − y)','F17':'f(x) = 1/x: المركز O، والمقاربان x = 0 و y = 0 محفوظان','F18':'الدالة العكسية: f(x) = eˣ و f⁻¹(x) = ln(x)، المرآة y = x','F19':'الدالة العكسية: مماس أفقي ↔ مماس عمودي — f(x) = (x − 1)³ + 1'}
EXL={'fr':'**Exemple :** ','en':'**Example:** ','ar':'**مثال:** '}
MARK='\u2060'; ARX={}
def reg(en,ar):
    k=en+MARK
    while k in ARX and ARX[k]!=ar: k+=MARK
    ARX[k]=ar; return k
def items(i,prev):
    k=D['en'][i][0]
    if k=='T':
        rows={l:D[l][i][1] for l in LG}
        rh=rows['en'][0][0].strip()=='x'
        return [{'dtab':{'fr':rows['fr'],'en':rows['en'],'ar':rows['ar'],'rh':rh,'ltr':rh}}]
    if k=='F':
        f=D['en'][i][1]; out=[]
        for tag in ('lt','dk'):
            out.append({'img':{'src':f'assets/trace/{f}_{tag}.png','fr':capfr[f],'en':reg(EN[f],AR[f])}})
        return out
    # paragraph
    txt={l:D[l][i][1] for l in LG}; c=D['en'][i][2]
    if c=='example' and prev!='example': txt={l:EXL[l]+txt[l] for l in LG}
    return [{'fr':txt['fr'],'en':reg(txt['en'],txt['ar'])}]
def stepsplit(blocks_idx):
    """split list of indices into sub-steps at '**N. heading**' paragraphs"""
    heads=[j for j,i in enumerate(blocks_idx) if D['en'][i][0]=='P' and re.match(r'\*\*\d+\. ',D['en'][i][1])]
    return heads
lessons=[]; cur=None; curs=None
def newlesson(i):
    global cur,curs
    cur={'id':f'tr-l{len(lessons)+1}','title':[D[l][i][1] for l in LG],'_pre':[],'_subs':[]}; lessons.append(cur); curs=None
for i in range(N):
    k=D['en'][i][0]
    if k=='L': newlesson(i)
    elif k=='S': curs={'t':[D[l][i][1] for l in LG],'idx':[]}; cur['_subs'].append(curs)
    else:
        if cur is None: newlesson(-1) if False else None
        (curs['idx'] if curs else cur['_pre']).append(i)
# the first block (Introduction) – parse() emitted L for '## Introduction'
def mk(title,idx):
    prev=None; bl=[]
    for i in idx:
        bl+=items(i,prev); prev=D['en'][i][2] if D['en'][i][0]=='P' else None
    return {'t':title,'story':{'fr':'','en':''},'blocks':bl,'apps':[]}
def hdtitle(i):
    return [re.sub(r'\.$','',re.match(r'\*\*\d+\.\s*(.*?)\*\*',D[l][i][1]).group(1).strip().rstrip('.:')) for l in LG]
out=[];nsteps=0
for L in lessons:
    groups=[]  # (title, idx)
    if L['_pre']: groups.append((L['title'],L['_pre']))
    for s in L['_subs']: groups.append((s['t'],s['idx']))
    steps=[]
    for t,idx in groups:
        h=stepsplit(idx)
        if len(h)>=3:
            if h[0]>0: steps.append(mk(t,idx[:h[0]]))
            for a,b in zip(h,h[1:]+[len(idx)]):
                tt=hdtitle(idx[a])
                if a==0 and h[0]==0:
                    nm=re.match(r'^(\d+\.\d+)',t[1])
                    if nm: tt=[nm.group(1)+' · '+x for x in tt]
                steps.append(mk(tt,idx[a:b]))
        else: steps.append(mk(t,idx))
    for j,s in enumerate(steps): s['id']=f's{j+1}'
    nsteps+=len(steps)
    out.append({'id':L['id'],'title':L['title'],'steps':steps})
print('lessons',len(out),'steps',nsteps)
for L in out: print(L['id'],ascii(L['title'][1]),[len(s['blocks']) for s in L['steps']])
js=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
T3={'trD':{'fr':"Asymptotes, branches paraboliques, tableaux de variation, concavité, position relative, parité, symétrie et fonction réciproque : tout pour tracer une courbe juste.",'en':"Asymptotes, parabolic branches, variation tables, concavity, relative position, parity, symmetry and the inverse function: everything to graph a curve correctly.",'ar':"المقاربات، الفروع الشلجمية، جداول التغيرات، التقعر، الوضع النسبي، الزوجية، التماثل والدالة العكسية: كل ما تحتاجه لرسم منحنى صحيح."}}
blk=("const TRLES="+js(out)+";\nObject.assign(ARX,"+js(ARX)+");\n"
 +''.join(f"T.{l}.trD={js(T3['trD'][l])};" for l in LG)+"\n"
 "CH.push({id:'trace',kind:'lesson',dk:'trD',title:[\"Tracé des fonctions\",\"Graphing functions\",\"رسم الدوال\"],lessons:TRLES,exercises:[],tracks:['PC','SM','SVT']});\n")
open('/home/claude/w/tr_block.js','w',encoding='utf-8').write(blk)
# ---- inject ----
bk=P+'backup/index.before-trace.html'
if not os.path.exists(bk): shutil.copy(P+'index.html',bk)
s=open(bk,encoding='utf-8').read()
m=re.search(r"CH\.push\(\{id:'suites'.*?tracks:\['PC','SM','SVT'\]\}\);\n",s,re.S); assert m
s=s[:m.end()]+blk+s[m.end():]
i0=s.find("${CH.filter(c=>c.id==='suites'"); assert i0>0 and s.count("${CH.filter(c=>c.id==='suites'")==1
i1=s.index(".join('')}",i0)+len(".join('')}")
old=s[i0:i1]
assert old.count("suites")==2 and old.count("suD")==1
s=s.replace(old,old+old.replace("suites","trace").replace("suD","trD"))
o2="LS.chapter==='racine'||LS.chapter==='suites'?' lwder'"
assert s.count(o2)==1
s=s.replace(o2,"LS.chapter==='racine'||LS.chapter==='suites'||LS.chapter==='trace'?' lwder'")
o3="les.id.indexOf('rn-')===0?' rnb':les.id.indexOf('su-')===0?' rnb sub':''"
assert s.count(o3)==1
s=s.replace(o3,"les.id.indexOf('rn-')===0?' rnb':les.id.indexOf('su-')===0?' rnb sub':les.id.indexOf('tr-')===0?' rnb sub':''")
css=('.coimg:has(img[src*="assets/trace/"]){background:transparent;border-color:transparent;padding:6px}.coimg img[src*="assets/trace/"]{max-width:min(100%,760px);mix-blend-mode:normal;filter:none}'
 '[data-theme=dark] .coimg:has(img[src*="_lt.png"][src*="assets/trace/"]),[data-theme=light] .coimg:has(img[src*="_dk.png"][src*="assets/trace/"]){display:none}')
anchor='.lwa[data-k^="rn-"]>p,.lwa[data-k^="ex:rn-"]>p{margin:10px 0}'
assert s.count(anchor)==1
s=s.replace(anchor,anchor+css)
open(P+'index.html','w',encoding='utf-8').write(s)
os.makedirs(P+'assets/trace',exist_ok=True)
src='/home/claude/w/spec/tracage_spec/assets/figures/'
for f in os.listdir(src):
    if f.endswith('.png'): shutil.copy(src+f,P+'assets/trace/'+f)
print('ok',len(s),len(os.listdir(P+'assets/trace')))
