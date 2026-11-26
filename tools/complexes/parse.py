"""Markdown -> flat block list, one parser for the FR / EN / AR sources of 'Les nombres complexes'."""
import re,os
SRC=os.environ.get('CX_SRC','/mnt/user-data/attachments/1172a3da-d14e-52ac-ae2c-05145723c309/')
FILES={'fr':'b7f4f959-Les_nombres_complexes.md','en':'e64fbb70-Complex_numbers_EN_full.md','ar':'766b7671-Les_nombres_complexes_AR_final.md'}
LIST=re.compile(r'^(\s*)(- |\d+[.)] )(.*)')
MARK=re.compile(r'^\[(USE|GRAPH|From|complex|COMPLEX)[^\]]*\]$',re.I)
def parse(lang):
    L=open(SRC+FILES[lang],encoding='utf-8').read().split('\n')
    i=0; out=[]; para=None
    def flush():
        nonlocal para
        if para: out.append(('P',0,' '.join(x.strip() for x in para))); para=None
    while i<len(L):
        l=L[i]; s=l.strip()
        if not s: flush(); i+=1; continue
        if l.startswith('#'):
            flush(); m=re.match(r'(#+)\s*(.*)',l); out.append(('H',len(m.group(1)),m.group(2).strip())); i+=1; continue
        if MARK.match(s):
            flush(); out.append(('IMG',0,s)); i+=1; continue
        if s=='$$' or (s.startswith('$$') and not (s.endswith('$$') and len(s)>3)):
            flush(); buf=[]
            if s=='$$':
                i+=1
                while L[i].strip()!='$$': buf.append(L[i].strip()); i+=1
            else:
                buf.append(s[2:])
                while not L[i].strip().endswith('$$'): i+=1; buf.append(L[i].strip())
                buf[-1]=re.sub(r'\$\$\s*$','',buf[-1])
            i+=1
            out.append(('M',0,'\n'.join(buf).strip())); continue
        if s.startswith('$$') and s.endswith('$$'):
            flush(); out.append(('M',0,s[2:-2].strip())); i+=1; continue
        m=LIST.match(l)
        if m:
            flush(); lvl=len(m.group(1))//3 if len(m.group(1))>=3 else (1 if m.group(1) else 0); mk=m.group(2).strip(); txt=m.group(3); i+=1
            while i<len(L) and L[i].strip() and not LIST.match(L[i]) and L[i].startswith('  ') and not L[i].strip().startswith('$$'):
                txt+=' '+L[i].strip(); i+=1
            out.append(('L',lvl,(mk,txt))); continue
        if s.startswith('|'):
            flush(); rows=[]
            while i<len(L) and L[i].strip().startswith('|'):
                r=L[i].strip()
                if not re.match(r'^\|[\s:|-]+\|$',r): rows.append([c.strip() for c in r.strip().strip('|').split('|')])
                i+=1
            out.append(('T',0,rows)); continue
        if s.startswith('>'):
            flush(); q=[]
            while i<len(L) and L[i].strip().startswith('>'):
                q.append(L[i].strip()[1:].strip()); i+=1
            # paragraphs separated by empty quote lines
            ps=[];cur=[]
            for x in q:
                if x: cur.append(x)
                elif cur: ps.append(' '.join(cur)); cur=[]
            if cur: ps.append(' '.join(cur))
            out.append(('Q',0,ps)); continue
        if para is None: para=[]
        para.append(s); i+=1
    flush(); return out
def sig(c): return (c[0],c[1] if c[0] in 'HL' else 0)
if __name__=='__main__':
    import difflib,collections
    P={k:parse(k) for k in FILES}
    for k,v in P.items(): print(k,len(v),dict(collections.Counter(c[0] for c in v)))
    en=P['en']
    for name in ('fr','ar'):
        o=P[name]; sm=difflib.SequenceMatcher(None,[sig(e) for e in en],[sig(e) for e in o],autojunk=False)
        for tag,i1,i2,j1,j2 in sm.get_opcodes():
            if tag!='equal': print(name,tag,'en',i1,i2,'|',j1,j2,[str(x)[:90] for x in en[i1:i2][:3]],[str(x)[:90] for x in o[j1:j2][:3]])
