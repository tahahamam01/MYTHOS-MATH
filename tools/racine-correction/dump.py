import json,re,sys
d=json.load(open('fr.json'))
def inl(xs):
    o=''
    for x in xs:
        t=x['t']
        if t=='Str': o+=x['c']
        elif t=='Space': o+=' '
        elif t in('SoftBreak',): o+=' '
        elif t=='LineBreak': o+=' ⏎ '
        elif t=='Math':
            tex=x['c'][1]
            tex=re.sub(r'\\sqrt\[\{?\\? ?2\}?\]\{',r'\\sqrt{',tex)
            o+=('$$' if x['c'][0]['t']=='DisplayMath' else '$')+tex+('$$' if x['c'][0]['t']=='DisplayMath' else '$')
        elif t in('Strong','Emph','Span','Underline','Strikeout','Superscript','Subscript','SmallCaps'): o+=inl(x['c'] if t!='Span' else x['c'][1])
        elif t=='Quoted': o+='"'+inl(x['c'][1])+'"'
        elif t=='Link': o+=inl(x['c'][1])
        else: o+='<%s>'%t
    return o
out=[]
def blk(b,ind=0,pre=''):
    t=b['t']; p='  '*ind
    if t in('Para','Plain'): out.append(p+pre+inl(b['c']))
    elif t=='Header': out.append(p+'#'*b['c'][0]+' '+inl(b['c'][2]))
    elif t=='OrderedList':
        st=b['c'][0][0]
        for i,it in enumerate(b['c'][1]):
            for j,bb in enumerate(it): blk(bb,ind+1,('[%d] '%(st+i)) if j==0 else '')
    elif t=='BulletList':
        for it in b['c']:
            for j,bb in enumerate(it): blk(bb,ind+1,'• ' if j==0 else '')
    elif t=='Table': out.append(p+'<TABLE> '+json.dumps(b['c'],ensure_ascii=False)[:50])
    elif t=='BlockQuote':
        for bb in b['c']: blk(bb,ind+1,'> ')
    else: out.append(p+'<%s>'%t)
for b in d['blocks']: blk(b)
open('dump.txt','w',encoding='utf8').write('\n'.join(out))
print(len(out))
