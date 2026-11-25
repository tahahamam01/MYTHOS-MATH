import re
SRC='/home/claude/p/'
FILES={'fr':'Les_Suites_FR_fixed.md','en':'Les_Suites_EN.md','ar':'Les_Suites_AR.md'}
def parse(lang):
    L=open(SRC+FILES[lang],encoding='utf-8').read().split('\n')
    i=0
    if L[0].strip()=='---':
        i=1
        while L[i].strip()!='---': i+=1
        i+=1
    out=[]; para=None
    def flush():
        nonlocal para
        if para: out.append(('P',0,' '.join(x.strip() for x in para))); para=None
    while i<len(L):
        l=L[i]; s=l.strip()
        if not s: flush(); i+=1; continue
        if s=='---': flush(); i+=1; continue
        if s.startswith('<!--'):
            flush()
            while '-->' not in L[i]: i+=1
            i+=1; continue
        if l.startswith('#'):
            flush(); m=re.match(r'(#+)\s*(.*)',l); out.append(('H',len(m.group(1)),m.group(2).strip())); i+=1; continue
        if s.startswith('`[IMAGE') or re.match(r'^`\[[^`]*\]`$',s):
            flush(); out.append(('IMG',0,s)); i+=1; continue
        if s=='$$' or (s.startswith('$$') and not (s.endswith('$$') and len(s)>3)):
            flush(); buf=[s]; 
            if s=='$$':
                i+=1
                while L[i].strip()!='$$': buf.append(L[i]); i+=1
                buf.append('$$')
            else:
                while not L[i].strip().endswith('$$') or i==len(L): i+=1; buf.append(L[i])
            i+=1
            body=' '.join(x.strip() for x in buf).strip()
            body=re.sub(r'^\$\$\s*|\s*\$\$$','',body)
            out.append(('M',0,body)); continue
        if s.startswith('$$') and s.endswith('$$'):
            flush(); out.append(('M',0,s[2:-2].strip())); i+=1; continue
        m=re.match(r'^(\s*)(- |\d+[.)] )(.*)',l)
        if m:
            flush(); lvl=len(m.group(1))//3; mk=m.group(2).strip()
            txt=m.group(3); i+=1
            # continuation lines (indented, not new item, not blank)
            while i<len(L) and L[i].strip() and not re.match(r'^(\s*)(- |\d+[.)] )',L[i]) and L[i].startswith('  ') and not L[i].strip().startswith('$$'):
                txt+=' '+L[i].strip(); i+=1
            out.append(('L',lvl,(mk,txt))); continue
        if s.startswith('|'):
            flush(); rows=[]
            while i<len(L) and L[i].strip().startswith('|'):
                r=L[i].strip()
                if not re.match(r'^\|[\s:|-]+\|$',r): rows.append([c.strip() for c in r.strip('|').split('|')])
                i+=1
            out.append(('T',0,rows)); continue
        if s.startswith('>'):
            flush(); out.append(('Q',0,s.lstrip('> ').strip())); i+=1; continue
        if para is None: para=[]
        para.append(s); i+=1
    flush(); return out
def sig(c): return (c[0],c[1] if c[0] in 'HL' else 0)
if __name__=='__main__':
    P={k:parse(k) for k in FILES}
    for k,v in P.items(): print(k,len(v))
    a,b,c=P['fr'],P['en'],P['ar']
    n=0
    for x,(y,z) in enumerate(zip(a,zip(b,c))):
        pass
    import difflib
    for name,o in (('fr',a),('ar',c)):
        sm=difflib.SequenceMatcher(None,[sig(e) for e in b],[sig(e) for e in o],autojunk=False)
        for tag,i1,i2,j1,j2 in sm.get_opcodes():
            if tag!='equal': print(name,tag,'en',i1,i2,'|',j1,j2, b[i1:i2][:2], o[j1:j2][:2])
