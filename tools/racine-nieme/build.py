import re,json,sys
from parse import chunks
from ex import exs
FRF='Racine_d_ordre_n_AI_ready_1.md';ENF='Nth_root_course_EN.md';ARF='Nth_root_course_AR.md'
APOS=lambda s:re.sub(r"(?<=\w)'(?=\w)","\u2019",s)
def nonmath(s,f):
    parts=re.split(r'(\$[^$]*\$)',s)
    return ''.join(p if p.startswith('$') and len(p)>1 else f(p) for p in parts)
def clean(s,lang):
    s=s.replace('`','')
    s=s.replace('(ajoutée) ','')
    if lang!='ar': s=nonmath(s,APOS)
    return s
def course(path):
    c=chunks(path); i=[k for k,x in enumerate(c) if x[0]=='H' and x[1].startswith('## 1.')][0]
    j=([k for k,x in enumerate(c) if x[0]=='H' and x[1].startswith('## 7')]+[len(c)])[0]
    c=c[i:j]
    return [x for x in c if not (x[0]=='P' and x[1].startswith('*(Énoncé corrigé'))]
def notes(path):
    t=open('/mnt/user-data/uploads/'+path,encoding='utf8').read()
    k=t.find('\n## 8.'); lines=t[k:].strip().split('\n')
    return lines[0][3:].strip(),[l[2:].strip() for l in lines if l.startswith('- ')]
def blocks_of(ch,lang):
    """chunk -> list of text blocks / ('T',rows)"""
    kind=ch[0]
    if kind=='T':
        rows=[[c.strip() for c in l.strip().strip('|').split('|')] for l in ch[1:] if not re.match(r'^\|[-| ]+\|$',l)]
        return [('T',[[clean(c,lang) for c in r] for r in rows])]
    if kind=='Q':
        t=' '.join(l.lstrip('> ').strip() for l in ch[1:]) if False else ' '.join(l[1:].strip() for l in ch[1:] if True)
        return [('X',clean(t,lang))]
    if kind=='M':
        t=' '.join(l.strip() for l in ch[1:]); 
        return [('X',clean(re.sub(r'^\$\$|\$\$$','',t.strip()).join(['$\\displaystyle ','$']),lang))]
    t=' '.join(l.strip() for l in ch[1:])
    if kind=='L':
        t=re.sub(r'^- ','• ',t)
    out=[]
    pos=0
    for m in re.finditer(r'\$\$(.*?)\$\$',t):
        pre=t[pos:m.start()].strip()
        if pre: out.append(('X',clean(pre,lang)))
        out.append(('X','$\\displaystyle '+m.group(1).strip()+'$'))
        pos=m.end()
    rest=t[pos:].strip()
    if rest: out.append(('X',clean(rest,lang)))
    return out
def heading(ch,lang):
    return clean(re.sub(r'^#+\s*','',ch[1]),lang)
LES=[ # lesson id, titles, section-number prefixes
 ('rn-l1',['Introduction et définition','Introduction and definition','تمهيد والتعريف'],('1.','2.')),
 ('rn-l2',['Propriétés','Properties','الخاصيات'],('3.',)),
 ('rn-l3',['Simplification des racines $n$-ièmes','Simplifying $n$-th roots','تبسيط الجذور من الرتبة $n$'],('4.',)),
 ('rn-l4',['Identités remarquables et équations','Remarkable identities and equations','المتطابقات الهامة والمعادلات'],('5.',)),
 ('rn-l5',['Limites avec racines','Limits with roots','النهايات والجذور'],('6.',)),
]
ARX={}
def build_lessons():
    F,E,A=course(FRF),course(ENF),course(ARF)
    assert len(F)==len(E)==len(A),(len(F),len(E),len(A))
    for a,b,c in zip(F,E,A): assert a[0]==b[0]==c[0],(a[:2],b[:2],c[:2])
    # walk
    lessons=[];cur=None;step=None;sec=None
    def newstep(t):
        nonlocal step
        step={'id':'s%d'%(len(cur['steps'])+1),'t':t,'story':{'fr':'','en':''},'blocks':[],'apps':[]}
        cur['steps'].append(step)
    for f,e,a in zip(F,E,A):
        if f[0]=='H':
            ft,et,at=heading(f,'fr'),heading(e,'en'),heading(a,'ar')
            m=re.match(r'(\d+)\.',et)
            if e[1].startswith('## ') and m:
                for lid,tt,pref in LES:
                    if et.startswith(pref):
                        if not(cur and cur['id']==lid):
                            cur={'id':lid,'title':tt,'steps':[]};lessons.append(cur)
                        break
            newstep([ft,et,at]); continue
        bf,be,ba=blocks_of(f,'fr'),blocks_of(e,'en'),blocks_of(a,'ar')
        assert len(bf)==len(be)==len(ba),(f[:2],e[:2])
        for x,y,z in zip(bf,be,ba):
            if x[0]=='T':
                step['blocks'].append({'dtab':{'fr':x[1],'en':y[1],'ar':z[1]}})
            else:
                step['blocks'].append({'fr':x[1],'en':y[1]}); 
                if y[1] in ARX and ARX[y[1]]!=z[1]: print('CONFLICT',y[1][:60],file=sys.stderr)
                ARX[y[1]]=z[1]
    # notes
    fh,fn=('8. Notes',[
     "**Indice pair** : racine définie seulement pour un radicande $\\ge 0$, résultat $\\ge 0$, et $\\sqrt[n]{x^n} = |x|$. **Indice impair** : définie sur $\\mathbb{R}$, $\\sqrt[n]{x^n} = x$.",
     "**Même indice** pour multiplier ou diviser des racines ; sinon, passer aux puissances rationnelles.",
     "$\\sqrt[n]{a+b} \\neq \\sqrt[n]{a} + \\sqrt[n]{b}$.",
     "Équations avec racines d’indice pair : toujours **vérifier** les solutions.",
     "Limites : substituer, puis utiliser un conjugué (carré : $a+b$ ; cubique : $a^2+ab+b^2$) ou factoriser le terme dominant."])
    eh,en_=notes(ENF); ah,an=notes(ARF); assert len(en_)==len(an)==5
    cur={'id':'rn-l6','title':['Notes à retenir','Notes to remember','ملاحظات للحفظ'],'steps':[]};lessons.append(cur)
    newstep([fh,eh.replace('## ',''),ah.replace('## ','')])
    for x,y,z in zip(fn,en_,an):
        step['blocks'].append({'fr':nonmath(x,APOS),'en':nonmath('• '+y,APOS)}); step['blocks'][-1]['fr']='• '+step['blocks'][-1]['fr']
        ARX[step['blocks'][-1]['en']]='• '+z
    # drop empty steps and renumber
    for l in lessons:
        l['steps']=[s for s in l['steps'] if s['blocks']]
        for i,s in enumerate(l['steps']): s['id']='s%d'%(i+1)
    return lessons

# ---------------- exercises ----------------
TIER={'CHICK':'ve','CHICKEN':'e','RAVEN':'m','EAGLE':'h','PHOENIX':'x'}
FRTR=[
 (r'Compute, if they exist','Calculer, si elles existent'),
 (r'Compute','Calculer'),(r'Write as a power','Écrire sous forme de puissance'),
 (r'Write as a root','Écrire sous forme de racine'),(r'Simplify','Simplifier'),
 (r'True or false\?','Vrai ou faux ?'),(r'Rationalise the denominator','Rationaliser le dénominateur'),
 (r'Compare:','Comparer :'),(r'Solve in','Résoudre dans'),(r'Solve:','Résoudre :'),(r'Solve','Résoudre'),
 (r'Domain of:','Domaine de définition de :'),(r'Limits:','Limites :'),(r'Show that','Montrer que'),
 (r'does not exist \(even index, negative radicand\)','n’existe pas (indice pair, radicande négatif)'),
 (r'does not exist','n’existe pas'),
 (r'the sum of roots is not the root of the sum','la somme des racines n’est pas la racine de la somme'),
 (r'Same equation as PHOENIX-01, so','Même équation que PHOENIX-01, donc'),
 (r'Check for','Vérification pour'),(r'Check:','Vérification :'),
 (r'and the quotient is','et le quotient vaut'),(r'so the denominator equals','donc le dénominateur vaut'),
 (r'the denominator is','le dénominateur est'),(r'the numerator becomes','le numérateur devient'),
 (r'the limit is','la limite vaut'),(r'is a root','est racine'),(r'is rejected','est rejeté'),
 (r'\(rejected\)','(rejeté)'),(r'rejected','rejeté'),(r'works','convient'),
 (r'Index','Indice'),(r'index','indice'),(r'condition','condition'),
 (r'Since','Comme'),(r'Hence','Donc'),(r'Likewise','De même'),(r'With','Avec'),(r'with','avec'),
 (r'Write','Écrire'),(r'write','écrire'),(r'gives','donne'),(r'equals','vaut'),
 (r'\bstatement\b','énoncé'),(r'\btrue\b','vrai'),(r'\bfalse\b','faux'),
 (r'\bsince\b','car'),(r'\bonly\b','seul'),(r'\bthen\b','alors'),(r'\band\b','et'),(r'\bor\b','ou'),(r'\bfor\b','pour'),
 (r'\bso\b','donc'),(r'\bSo\b','Donc'),(r'\bHence\b','Donc'),(r'\bAt\b','En'),(r'\bFor\b','Pour'),
]
def fr_tr(s):
    s=s.replace('`','')
    def f(p):
        for a,b in FRTR: p=re.sub(a,b,p)
        return p
    s=nonmath(s,f)
    s=nonmath(s,lambda p:re.sub(r'(?<=[^\s:]):(?=\s|$)',' :',re.sub(r'(?<!\s);',' ;',p)))
    return nonmath(s,APOS)
def en_clean(s): return nonmath(s.replace('`',''),APOS)
def build_exercises():
    en,wE,_=exs(ENF); ar,wA,_=exs(ARF)
    out=[]
    for (i,s,so),(j,s2,so2) in zip(en,ar):
        assert i==j
        tier,n=i.split('-')
        eid='rn-%s-%s'%(tier.lower(),n)
        pe,se=en_clean(s),en_clean(so)
        pf,sf=fr_tr(s),fr_tr(so)
        ARX[pe]=s2.replace('`',''); ARX[se]=so2.replace('`','')
        e={'id':eid,'d':TIER[tier],'p':{'fr':pf,'en':pe},'q':'','sol':[{'fr':sf,'en':se}]}
        if i=='EAGLE-01':
            wf=("**Avertissements propres à ce niveau.** (1) Le conjugué d’une racine cubique est $a^2 + ab + b^2$, **et non** $a+b$. "
                "(2) En $-\\infty$, $\\sqrt{x^2} = |x| = -x$ et $\\sqrt[4]{x^4} = |x|$ : attention au signe. "
                "(3) Essayer d’abord la substitution : n’utiliser un conjugué que si la forme est indéterminée.")
            we=en_clean(wE.strip()); ARX[we]=wA.strip()
            e['blocks']=[{'fr':wf,'en':we}]
        out.append(e)
    return out

def emit():
    L=build_lessons(); X=build_exercises()
    ids=[e['id'] for e in X]
    main=[i for i in ids if '-phoenix-' not in i]; opt=[i for i in ids if '-phoenix-' in i]
    j=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
    code=("\n/* ===== RACINE N-IÈME — PC / SM / SVT (content from Racine_d_ordre_n_AI_ready_1.md FR / Nth_root_course_EN.md / Nth_root_course_AR.md; same engine as Continuité) ===== */\n"
     "const RNLES="+j([{'id':l['id'],'title':l['title'],'steps':l['steps']} for l in L])+";\n"
     "const RNEX="+j(X)+";\n"
     "RNEX.forEach(e=>{e.ex=true;EXB[e.id]=e});\n"
     "Object.assign(ARX,"+j(ARX)+");\n"
     "T.fr.rnD=\"Définition, propriétés, simplification, équations et limites avec racines n-ièmes.\";T.en.rnD=\"Definition, properties, simplification, equations and limits with n-th roots.\";T.ar.rnD=\"التعريف، الخاصيات، التبسيط، المعادلات والنهايات التي تحتوي على جذور من الرتبة n.\";\n"
     "CH.push({id:'racine',kind:'lesson',dk:'rnD',title:[\"Racine n-ième\",\"Nth roots\",\"الجذر من الرتبة n\"],lessons:RNLES,exercises:"+j(main)+",optional:"+j(opt)+",tracks:['PC','SM','SVT']});\n")
    return code
if __name__=='__main__':
    open('/home/claude/work/rn_block.js','w',encoding='utf8').write(emit())
    print(len(emit()))
