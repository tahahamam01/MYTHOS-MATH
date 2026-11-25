import re
U='/mnt/user-data/uploads/'
def load(l):
    t=open(U+{'fr':'SPECTRACAGE.md','en':'SPECTRACAGE_EN.md','ar':'SPECTRACAGE_AR.md'}[l],encoding='utf-8').read()
    if l=='fr':
        i=t.find('# Tracé des fonctions'); j=t.find('\n## 4. Figure details'); t=t[i:j]
    return t
def clean(s):
    s=s.replace('`','')
    s=re.sub(r'\*\(.*?\)\*','',s)
    s=re.sub(r'\s*\((?:added example|exemple ajouté|مثال مضاف)[^)]*\)','',s)
    s=s.replace('of the added example','of the example').replace("de l'exemple ajouté","de l'exemple").replace('المثال المضاف','المثال')                    # editorial *(...)*
    s=re.sub(r'\s*[→←]\s*\*?F\d+[^*\n]*\*?(?=\s*$|\s*[.;])','',s)
    s=re.sub(r'\s*—\s*\*[^*]*\*\s*$','',s)           # trailing "— *note*"
    return s.strip()
def ital(s):
    return re.sub(r'(?<!\*)\*(?!\*)([^*\n]+?)(?<!\*)\*(?!\*)',r'**\1**',s)
def parse(l):
    L=load(l).split('\n'); out=[]; i=0; para=[]; callout=None; first=False
    def flush():
        nonlocal para,first
        if para:
            out.append(('P',' '.join(para),callout)); para=[]
    while i<len(L):
        ln=L[i]; st=ln.strip(); i+=1
        if not st: flush(); continue
        if st.startswith(':::'):
            flush(); callout=st[3:] or None
            if not callout: pass
            continue
        if st=='---': flush(); continue
        if st.startswith('# '): flush(); continue
        if st.startswith('## '): flush(); out.append(('L',st[3:].strip())); continue
        if st.startswith('### '): flush(); out.append(('S',st[4:].strip())); continue
        if st.startswith('|'):
            flush(); rows=[]
            i-=1
            while i<len(L) and L[i].strip().startswith('|'):
                r=L[i].strip().strip('|').split('|'); i+=1
                if all(re.fullmatch(r'\s*:?-+:?\s*',c) for c in r): continue
                rows.append([c.strip() for c in r])
            out.append(('T',rows)); continue
        m=re.match(r'^(\s*)([*-]|\d+\.)\s+(.*)$',ln)
        if m:
            flush(); lv=len(m.group(1))//2; mk=m.group(2)
            pre='\u2003'*2*lv+('• ' if lv==0 else '– ') if mk in '*-' else '\u2003'*2*lv+mk+' '
            out.append(('P',pre+m.group(3).strip(),callout)); continue
        if st.startswith('> '): flush(); out.append(('P',st[2:],callout)); continue
        para.append(st)
    flush()
    # post: split figures, clean, drop empties; label first para of example callouts
    res=[]; seenF=set(); prevc=None
    for it in out:
        if it[0] in 'LS': res.append((it[0],it[1].strip())); prevc=None; continue
        if it[0]=='T':
            res.append(('T',[[clean(c) for c in r] for r in it[1]])); continue
        txt,c=it[1],it[2]
        if re.match(r'^\*(Implementation note|Table of this last|Note d.impl|Tableau de ce)',txt) : continue
        parts=re.split(r'<<FIGURE (F\d+)>>',txt.replace('`',''))
        for k,p in enumerate(parts):
            if k%2:
                if p not in seenF: seenF.add(p); res.append(('F',p))
                continue
            p=clean(p); p=re.sub(r'^[\s·—–-]+|[\s·—–→-]+$','',p) if k>0 or len(parts)>1 else p
            p=re.sub(r'(?<=\S)\s*→\s*$','',p)
            if p and not re.fullmatch(r'[\s·—–→*]*',p):
                res.append(('P',ital(p),c if k==0 else None))
    return res
if __name__=='__main__':
    P={l:parse(l) for l in ('fr','en','ar')}
    for l in P: print(l,len(P[l]))
    n=min(len(v) for v in P.values())
    for k in range(n):
        a,b,c=P['fr'][k],P['en'][k],P['ar'][k]
        if not (a[0]==b[0]==c[0]) or (a[0]=='L' and False):
            print('MISMATCH',k,[x[0] for x in (a,b,c)],[ascii(str(x[1])[:50]) for x in (a,b,c)]); break
