import re
U='/mnt/user-data/uploads/'
def chunks(path):
    L=open(U+path,encoding='utf8').read().split('\n')
    out=[];cur=None;sec=None
    def flush():
        nonlocal cur
        if cur is not None: out.append(cur); cur=None
    i=0
    while i<len(L):
        l=L[i]
        if l.startswith('---') and i<14: i+=1;continue
        if l.startswith('#'):
            flush(); out.append(('H',l)); i+=1; continue
        if not l.strip() or l.strip()=='---': flush(); i+=1; continue
        if l.startswith('$$') and not l.rstrip().endswith('$$') or l.strip()=='$$':
            flush(); cur=['M',l]; i+=1; continue
        if re.match(r'^(- |\d+\. )',l):
            flush(); cur=['L',l]; i+=1; continue
        if l.startswith('|'):
            if cur is None or cur[0]!='T': flush(); cur=['T',l]
            else: cur.append(l)
            i+=1; continue
        if l.startswith('>'):
            if cur is None or cur[0]!='Q': flush(); cur=['Q',l]
            else: cur.append(l)
            i+=1; continue
        if cur is not None and cur[0] in 'LM' and (l.startswith('   ') or cur[0]=='M'):
            cur.append(l); i+=1; continue
        if cur is not None and cur[0]=='L' and False: pass
        if cur is not None and cur[0]=='P': cur.append(l); i+=1; continue
        flush(); cur=['P',l]; i+=1
    flush(); return out
if __name__=='__main__':
    for f in ['Racine_d_ordre_n_AI_ready_1.md','Nth_root_course_EN.md','Nth_root_course_AR.md']:
        c=chunks(f)
        # stop at exercises heading
        idx=[k for k,x in enumerate(c) if x[0]=='H' and (x[1].startswith('## 7'))]
        c=c[:idx[0]] if idx else c
        print(f,len(c),[ (k,x[0]) for k,x in enumerate(c) if x[0]=='H'][:30])
