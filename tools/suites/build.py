import re,json,sys
from sparse import parse
LG=('fr','en','ar')
P={k:parse(k) for k in LG}
F,E,A=P['fr'],P['en'],P['ar']
N=len(E)
for i in range(N): assert F[i][0]==E[i][0]==A[i][0] and (E[i][0] not in 'HL' or F[i][1]==E[i][1]==A[i][1]),(i,F[i][:2],E[i][:2],A[i][:2])
W={'fr':F,'en':E,'ar':A}
MARK='\u2060'
ARX={}      # en-key -> ar
REPORT={'splits':[],'arconflict':0,'mathdiff':[],'dropped':[]}
def reg(en,ar):
    k=en
    while k in ARX and ARX[k]!=ar: k+=MARK
    if k==en: k=en+MARK
    while k in ARX and ARX[k]!=ar: k+=MARK
    ARX[k]=ar; return k
def nonmath(s,f):
    return ''.join(p if (p.startswith('$') and len(p)>1 and p.endswith('$')) else f(p) for p in re.split(r'(\$[^$]*\$)',s))
ital=lambda p:re.sub(r'(?<!\*)\*(?!\*)([^*\n]+?)(?<!\*)\*(?!\*)',r'**\1**',p)
def cl(s):
    s=s.replace('`','')
    s=re.sub(r'\s*\*\*\[R\d+\]\*\*','',s); s=re.sub(r'\s*\[R\d+\]','',s)
    return nonmath(s,ital).strip()
def puremath(s):
    m=re.fullmatch(r'\$([^$]+)\$\s*[.,;]?',s.strip()); return m.group(1).strip() if m else None
def lead(c):
    if c[0]!='P': return None
    m=re.match(r'\*\*([^*]*)\*\*',c[2]); return m.group(1) if m else ''
def strip_label(t):
    return re.sub(r'^\*\*[^*]*\*\*\s*','',t)
# ---------- item builders (internal: dict) ----------
def T3(fr,en,ar): return {'k':'t','fr':fr,'en':en,'ar':ar}
def X3(tex): return {'k':'x','tex':tex}
def textitems(idx,texts=None,prefix=('','','')):
    """texts: optional override (fr,en,ar) raw strings. returns list of items (splits inline $$)."""
    raw=texts or tuple(W[l][idx][2] if W[l][idx][0]!='L' else W[l][idx][2][1] for l in LG)
    raw=[cl(r) for r in raw]
    if any('$$' in r for r in raw):
        parts=[re.split(r'\$\$(.*?)\$\$',r) for r in raw]
        assert len({len(p) for p in parts})==1
        out=[]
        for j in range(len(parts[0])):
            if j%2: out.append(X3(parts[1][j].strip()))
            else:
                tx=[ (prefix[n] if j==0 else '')+parts[n][j].strip() for n in range(3)]
                if any(t.strip() for t in tx): out.append(T3(*tx))
        return out
    pm=[puremath(r) for r in raw]
    if all(pm) and not any(prefix):
        if len(set(pm))>1:
            REPORT['mathdiff'].append((idx,pm)); return [T3(*['$\\displaystyle '+x+'$' for x in pm])]
        return [X3(pm[0])]
    return [T3(*[prefix[n]+raw[n] for n in range(3)])]
def conv(idxs,sol=False):
    out=[];prev=None;i=0
    while i<len(idxs):
        idx=idxs[i]; c=E[idx]; k=c[0]
        if k=='P': out+=textitems(idx); prev='P'
        elif k=='M':
            tex=[W[l][idx][2] for l in LG]
            if len(set(t_.strip() for t_ in tex))>1:
                REPORT['mathdiff'].append((idx,tex)); out.append(T3(*['$\\displaystyle '+t_.strip()+'$' for t_ in tex]))
            else: out.append(X3(tex[0].strip()))
            prev='M'
        elif k=='L':
            mk=c[2][0]; lvl=c[1]
            if sol and mk=='-' and lvl==0 and prev in ('N','P'): lvl=1
            ind='\u2003'*2*lvl
            pf=[ind+('• ' if lvl==0 else '– ')]*3 if mk=='-' else [ind+W[l][idx][2][0]+' ' for l in LG]
            out+=textitems(idx,prefix=tuple(pf)); prev='N' if mk!='-' else ('B' if prev not in('N','P') else prev if False else 'B')
            if mk!='-': prev='N'
        elif k=='T':
            rows={l:[[cl(x) for x in r] for r in W[l][idx][2]] for l in LG}
            hd=rows['en'][0][0]==''
            out.append({'k':'tab','rows':rows,'rh':hd}); prev='T'
        elif k=='IMG':
            out.append({'k':'img','n':sum(1 for o in out if o['k']=='img')}); prev='I'
        elif k=='H':
            out.append(T3(*['**'+cl(W[l][idx][2])+'**' for l in LG])); prev='P'
        elif k=='Q': REPORT['dropped'].append(('Q',idx,c[2][:80]))
        else: raise Exception((k,idx))
        i+=1
    return out
# ---------- lessons ----------
ex_start=[i for i,c in enumerate(E) if c[0]=='H' and c[1]==2 and c[2].startswith('CHICK')][0]
first=[i for i,c in enumerate(E) if c[0]=='H' and c[1]==2 and re.match(r'\d+\.',c[2])][0]
H=lambda i:[cl(re.sub(r'^\d+\.\s+','',W[l][i][2])) if W[l][i][1]==2 else cl(W[l][i][2]) for l in LG]
lessons=[]
for i in range(first,ex_start):
    c=E[i]
    if c[0]=='H' and c[1]==2:
        lessons.append({'title':H(i),'steps':[]})
    elif c[0]=='H' and c[1]==3:
        lessons[-1]['steps'].append({'t':H(i),'raw':[],'cont':c[2].startswith('Application')})
    elif c[0]=='H' and c[1]==1: continue
    else:
        L_=lessons[-1]
        if not L_['steps']: L_['steps'].append({'t':L_['title'],'raw':[],'cont':False})
        L_['steps'][-1]['raw'].append(i)
SOLRE=re.compile(r'^(Solution|Detailed solution)')
ENDRE=re.compile(r'^(Example|Application|Method|Remark|Warning|Info|Note|Key|Summary|Complete|Formula|Pitfalls|Why|Where|How|If|Given|Questions|An example)')
LABRE={'fr':r'^Application(?: avec correction)?(?: \d+)?','en':r'^Application(?: with solution)?(?: \d+)?','ar':r'^تطبيق(?: مع التصحيح)?(?: \d+)?'}
STMT=re.compile(r'^(Statement|Énoncé|نص التمرين)\s*[:.]\s*')
apps=[]
def solstart(idx):
    """items from a solution-marker paragraph (remainder after label)"""
    texts=[]
    for l in LG:
        m=re.match(r'\*\*[^*]*\*\*\s*(.*)$',W[l][idx][2]); texts.append(m.group(1) if m else W[l][idx][2])
    return textitems(idx,texts=tuple(texts)) if all(t.strip() for t in texts) else []
def make_app(stmt_idx,sol_idx,container):
    items=[]
    p=None; blocks=[]
    if not container:
        idx=stmt_idx[0]; labs=[];rests=[]
        for l in LG:
            m=re.match(r'\*\*([^*]*)\*\*\s*(.*)$',W[l][idx][2]); lab,rest=m.group(1),m.group(2)
            lab=re.sub(LABRE[l],'',lab).strip(' .:'); labs.append(lab); rests.append(STMT.sub('',rest))
        q=[('**'+x+'**') if x else '' for x in labs]
        first=textitems(idx,texts=tuple(rests)) if all(r.strip() for r in rests) else []
        rest_items=conv(stmt_idx[1:])
        if any(q): p=T3(*q); blocks=first+rest_items
        else:
            if first and first[0]['k']=='t': p=first[0]; blocks=first[1:]+rest_items
            else: blocks=first+rest_items
    else:
        its=conv(stmt_idx)
        if its and its[0]['k']=='t': p=its[0]; blocks=its[1:]
        else: blocks=its
    sol=solstart(sol_idx[0])+conv(sol_idx[1:],sol=True)
    return {'p':p,'blocks':blocks,'sol':sol}
def process(st):
    raw=st['raw']; segs=[]; cur=[]; i=0
    def isapp(idx): return (lead(E[idx]) or '').startswith('Application') and E[idx][0]=='P'
    def issol(idx): return E[idx][0]=='P' and bool(SOLRE.match(lead(E[idx]) or ''))
    if st['cont'] and not any(isapp(x) for x in raw):
        si=[k for k,x in enumerate(raw) if issol(x)]; assert si,st['t']
        segs.append(('app',make_app(raw[:si[0]],raw[si[0]:],True))); raw=[]
    while i<len(raw):
        idx=raw[i]
        if isapp(idx):
            if cur: segs.append(('blk',cur)); cur=[]
            j=i+1
            while j<len(raw) and not issol(raw[j]): j+=1
            assert j<len(raw),('no solution',idx)
            k=j+1
            while k<len(raw):
                l=lead(E[raw[k]]) if E[raw[k]][0]=='P' else None
                if l is not None and ENDRE.match(l) and not SOLRE.match(l): break
                k+=1
            segs.append(('app',make_app(raw[i:j],raw[j:k],False))); i=k
        else: cur.append(idx); i+=1
    if cur: segs.append(('blk',cur))
    # build substeps: each = blocks + apps; new substep after an app when more blocks follow
    subs=[{'blocks':[],'apps':[]}]
    for kind,v in segs:
        if kind=='blk':
            if subs[-1]['apps']: subs.append({'blocks':[],'apps':[]})
            subs[-1]['blocks']+=v
        else: subs[-1]['apps'].append(v)
    return subs
AID=0;LES=[]
CONT=('(suite)','(continued)','(تابع)')
for n,L_ in enumerate(lessons,1):
    steps=[]
    for st in L_['steps']:
        subs=process(st)
        for si,sb in enumerate(subs):
            t=st['t'] if si==0 else [st['t'][x]+' '+CONT[x] for x in range(3)]
            if si>0: REPORT['splits'].append((n,st['t'][1]))
            steps.append({'t':t,'blocks':conv(sb['blocks']),'apps':sb['apps']})
    LES.append({'id':'su-l%d'%n,'title':L_['title'],'steps':steps})
# ---------- exercises ----------
TIER={'CHICK':'ve','CHICKEN':'e','RAVEN':'m','EAGLE':'h','PHOENIX':'x'}
exs=[];i=ex_start;cur=None
while i<N:
    c=E[i]
    if c[0]=='H' and c[1]==3:
        m=re.match(r'(CHICKEN|CHICK|RAVEN|EAGLE|PHOENIX)-(\d+)\s*(?:\((.*)\))?',c[2])
        if m: cur={'tier':m.group(1),'n':m.group(2),'suf':m.group(3),'hi':i,'raw':[]}; exs.append(cur)
        else: cur=None
    elif c[0]=='H' and c[1]==2:
        if not re.match(r'(CHICKEN|CHICK|RAVEN|EAGLE|PHOENIX) Level',c[2]): cur=None
    elif cur is not None: cur['raw'].append(i)
    i+=1
THEME={}
for l in LG:
    for ex in exs:
        if ex['tier']=='EAGLE':
            last=W[l][ex['raw'][-1]][2]
            m=re.match(r'\*([^:*]+):',last)
            if m: THEME[l]=m.group(1).strip(); break
print('theme words',THEME,file=sys.stderr)
EXL=[]
for ex in exs:
    raw=ex['raw']
    si=[k for k,x in enumerate(raw) if E[x][0]=='P' and SOLRE.match(lead(E[x]) or '')]; assert si,(ex['tier'],ex['n'])
    st,so=raw[:si[0]],raw[si[0]:]
    assert E[st[0]][0]=='P' and (lead(E[st[0]]) or '').startswith('Statement'),(ex['tier'],ex['n'],E[st[0]])
    first=textitems(st[0],texts=tuple(strip_label(W[l][st[0]][2]) for l in LG)) if all(strip_label(W[l][st[0]][2]).strip() for l in LG) else []
    its=first+conv(st[1:])
    p=None;blocks=its
    if its and its[0]['k']=='t': p=its[0];blocks=its[1:]
    sol=solstart(so[0])+conv(so[1:],sol=True)
    if ex['suf']:
        # heading qualifier (kept as in the author's convention: theme line at the end of the correction)
        suf=[cl(re.search(r'\((.*)\)',W[l][ex['hi']][2]).group(1)) for l in LG]
        sol.append(T3(*['**'+THEME[l]+' : '+suf[n]+'**' if l=='fr' else '**'+THEME[l]+': '+suf[n]+'**' for n,l in enumerate(LG)]))
    EXL.append({'id':'su-%s-%s'%(ex['tier'].lower(),ex['n']),'d':TIER[ex['tier']],'p':p,'blocks':blocks,'sol':sol})
# ---------- finalise to JSON ----------
IMG={0:'assets/suites/dominoes_black.png',1:'assets/suites/dominoes_white.png'}
IMGALT=({'fr':'Une rangée infinie de dominos','en':'An infinite row of dominoes','ar':'صف لا نهائي من قطع الدومينو'})
def fin_item(it):
    if it['k']=='t':
        d={'fr':it['fr'],'en':it['en']}
        if it['ar'] and it['ar']!=it['en'] and it['ar']!=it['fr']: d['en']=reg(it['en'],it['ar'])
        return d
    if it['k']=='x': return {'x':it['tex']}
    if it['k']=='tab':
        r=it['rows']; d={'dtab':{'fr':r['fr'],'en':r['en'],'ar':r['ar']}}
        if it['rh']: d['dtab']['rh']=1
        return d
    if it['k']=='img':
        en=IMGALT['en']; return {'img':{'src':IMG[it['n']],'fr':IMGALT['fr'],'en':reg(en,IMGALT['ar'])}}
def fin_list(l): return [fin_item(x) for x in l]
APPS=[]
for les in LES:
    for st in les['steps']:
        ids=[]
        for ap in st['apps']:
            AID+=1; aid='su-app%d'%AID; ids.append(aid)
            d={'id':aid,'own':True}
            if ap['p']: d['p']=fin_item(ap['p'])
            d['q']=''
            d['blocks']=fin_list(ap['blocks']); d['sol']=fin_list(ap['sol'])
            APPS.append(d)
        st['apps']=ids; st['blocks']=fin_list(st['blocks'])
        st['story']={'fr':'','en':''}
for i_,s in enumerate([s for l in LES for s in l['steps']]): pass
for les in LES:
    for k,st in enumerate(les['steps'],1): st['id']='s%d'%k
EXOUT=[]
for e in EXL:
    d={'id':e['id'],'d':e['d']}
    if e['p']: d['p']=fin_item(e['p'])
    d['q']=''
    if e['blocks']: d['blocks']=fin_list(e['blocks'])
    d['sol']=fin_list(e['sol']); EXOUT.append(d)
# order keys like Continuité
def ordstep(s): return {'id':s['id'],'t':s['t'],'story':s['story'],'blocks':s['blocks'],'apps':s['apps']}
LESOUT=[{'id':l['id'],'title':l['title'],'steps':[ordstep(s) for s in l['steps']]} for l in LES]
j=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
main=[e['id'] for e in EXOUT if '-phoenix-' not in e['id']]; opt=[e['id'] for e in EXOUT if '-phoenix-' in e['id']]
code=("\n/* ===== LES SUITES — PC / SM / SVT (content from Les_Suites_FR_fixed.md / Les_Suites_EN.md / Les_Suites_AR.md; same engine as Continuité) ===== */\n"
 "const SULES="+j(LESOUT)+";\n"
 "const SUAPPS="+j(APPS)+";SUAPPS.forEach(a=>APPBANK[a.id]=a);\n"
 "const SUEX="+j(EXOUT)+";\nSUEX.forEach(e=>{e.ex=true;EXB[e.id]=e});\n"
 "Object.assign(ARX,"+j(ARX)+");\n"
 "T.fr.suD=\"Suites numériques : récurrence, suites arithmétiques et géométriques, convergence, limites, télescopage, suites adjacentes et suites de la forme $u_{n+1}=f(u_n)$.\";T.en.suD=\"Sequences: recurrence, arithmetic and geometric sequences, convergence, limits, telescoping, adjacent sequences and sequences of the form $u_{n+1}=f(u_n)$.\";T.ar.suD=\"المتتاليات العددية: البرهان بالترجع، المتتاليات الحسابية والهندسية، التقارب، النهايات، الاختزال، المتتاليتان المتجاورتان والمتتاليات من الشكل $u_{n+1}=f(u_n)$.\";\n"
 "CH.push({id:'suites',kind:'lesson',dk:'suD',title:[\"Les Suites\",\"Sequences\",\"المتتاليات\"],lessons:SULES,exercises:"+j(main)+",optional:"+j(opt)+",tracks:['PC','SM','SVT']});\n")
open('/home/claude/p/su_block.js','w',encoding='utf-8').write(code)
print('lessons',len(LESOUT),[len(l['steps']) for l in LESOUT],file=sys.stderr)
print('apps',len(APPS),'exercises',len(EXOUT),{t:sum(1 for e in EXOUT if e['d']==t) for t in ('ve','e','m','h','x')},file=sys.stderr)
print('ARX',len(ARX),'size',len(code),file=sys.stderr)
print('splits',REPORT['splits'],file=sys.stderr)
print('mathdiff',len(REPORT['mathdiff']),REPORT['mathdiff'][:3],file=sys.stderr)
print('dropped',REPORT['dropped'],file=sys.stderr)
