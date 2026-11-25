import re
U='/mnt/user-data/uploads/'
def exs(path):
    t=open(U+path,encoding='utf8').read()
    a=t.find('\n## 7.'); b=t.find('\n## 8.')
    body=t[a:b]; notes=t[b:]
    out=[];warn=None
    for m in re.finditer(r'\*\*`((?:CHICKEN|CHICK|RAVEN|EAGLE|PHOENIX)-\d\d)`\*\* — \*\*[^*]+\*\*\s*(.*?)\n\*\*[^*]+\*\*\s*(.*?)(?=\n\n|\Z)',body,re.S):
        out.append((m.group(1),m.group(2).strip(),m.group(3).strip()))
    wm=re.search(r'\n> (.*?)\n',body); warn=wm.group(1) if wm else None
    return out,warn,notes
if __name__=='__main__':
    en,w,n=exs('Nth_root_course_EN.md'); ar,w2,n2=exs('Nth_root_course_AR.md')
    print(len(en),len(ar),[e[0] for e in en]==[e[0] for e in ar]); print(w);print(w2)
    frag=set()
    for _,s,so in en:
        for txt in (s,so):
            for i,p in enumerate(re.split(r'\$[^$]*\$',txt)):
                p=p.strip(' ,;:.()')
                if re.search('[A-Za-z]{2,}',p): frag.add(p)
    for f in sorted(frag): print(repr(f))
    print(n)
