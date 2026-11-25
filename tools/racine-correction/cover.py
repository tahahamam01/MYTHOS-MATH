import json,re
d=json.load(open('fr.json'))
def flat(xs):
    r=''
    for x in xs:
        t=x['t']
        if t=='Str': r+=x['c']
        elif t=='Space': r+=' '
        elif t=='Math': r+='\x00'+x['c'][1]+'\x01'
        elif t in('Strong','Emph','Underline','Superscript','Subscript'): r+=flat(x['c'])
        elif t=='Span': r+=flat(x['c'][1])
        elif t in('SoftBreak','LineBreak'): r+=' '
    return r
src=[]
def addtxt(s):
    for m in re.finditer('\x00(.*?)\x01',s,re.S): src.append(m.group(1))
    s2=re.sub('\x00.*?\x01',' ',s,flags=re.S)
    for m in re.finditer(r'\$\$(.+?)\$\$|\$(.+?)\$',s2): src.append(m.group(1) or m.group(2))
def walk(b):
    t=b['t']
    if t in('Para','Plain'): addtxt(flat(b['c']))
    elif t=='OrderedList':
        for it in b['c'][1]:
            for bb in it: walk(bb)
    elif t=='BulletList':
        for it in b['c']:
            for bb in it: walk(bb)
    elif t=='BlockQuote':
        for bb in b['c']: walk(bb)
    elif t=='Header': addtxt(flat(b['c'][2]))
started=False
for b in d['blocks']:
    if b['t'] in('Para','Plain') and 'EXERCICES' in flat(b['c']): started=True
    if started: walk(b)
def norm(s):
    s=re.sub(r'\\sqrt\[\{?\\? ?2\}?\]\{',r'\\sqrt{',s)
    s=re.sub(r'\\sqrt\[\{\\ (\d+)\}\]',r'\\sqrt[\1]',s); s=s.replace('\\sqrt{\\ ','\\sqrt{')
    s=s.replace('\\rightarrow','\\to').replace('\\lbrack','[').replace('\\rbrack',']').replace('\\Rightarrow\\ ','\\Rightarrow ')
    s=re.sub(r'\\[dt]?frac','\\\\frac',s)
    s=s.replace('\\left','').replace('\\right','').replace('\\ ','').replace('\\,','').replace('\\mathbf','')
    s=re.sub(r'\s+','',s); s=s.replace('{,}',',')
    return s
EX=json.load(open('fr_final.json',encoding='utf8'))
mine=[]
for e in EX:
    for k in('stmt','sol'):
        for it in e[k]:
            if 'x' in it: mine.append(it['x'])
            else: mine+=it['m']
big=''.join(norm(m) for m in mine)
miss=[f for f in src if norm(f) and norm(f) not in big]
print('source math fragments in exercise section:',len(src),'| not found verbatim in final data:',len(miss))
for f in miss: print('  MISS:',f[:150])
