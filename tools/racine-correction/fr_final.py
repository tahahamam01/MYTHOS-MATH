import json,re
EX=json.load(open('fr_raw.json',encoding='utf8'))
D={e['id']:e for e in EX}
def T(t,*m): return {'t':t,'m':list(m)}
def X(x): return {'x':x}
# ---- overrides ----
D['RAVEN-05']['sol'][1]=T('{1} avec {2}',r'\dfrac{x^2+1}{a^2+ax+x^2}=\dfrac{1+\dfrac1{x^2}}{u^{2/3}+u^{1/3}+1}',r'u=1+\tfrac1x+\tfrac1{x^3}\to1')
D['RAVEN-07']['sol'][1]=T('{1} et {2}',r'a-1=\dfrac{x}{a^{2}+a+1}',r'c-1=\dfrac{2x}{c^{2}+c+1}')
D['EAGLE-01']['sol'][1]=T('{1}, {2}, {3}',r'a+b-2=(a-1)+(b-1)',r'a-1=\dfrac{x}{a^{2}+a+1}',r'b-1=\dfrac{-x}{b^{2}+b+1}')
assert 'b = 0oub' in D['EAGLE-06']['sol'][3]['x']
D['EAGLE-06']['sol'][3]=T('{1} ou {2}',r'(b+2)^{2}+(b+2)b+b^{2}=3b^{2}+6b+4=4\Rightarrow 3b(b+2)=0\Rightarrow b=0','b=-2')
D['EAGLE-11']['sol'][5]=T('{1} ou {2}',r'(a,b)=(7,2)',r'(a,b)=(-9,-2)')
assert '1etf' in D['EAGLE-12']['sol'][1]['x']
D['EAGLE-12']['sol'][1]=T('{1} et {2}',r'\dfrac{f(x)}{x}=1+\dfrac{1}{\sqrt[3]{x}}\to1',r'f(x)-x=\sqrt[3]{x^{2}}\to+\infty')
D['EAGLE-11']['sol'][11]['t']='**Discussion en {1} :**'
D['EAGLE-05']['stmt']=[X(D['EAGLE-05']['stmt'][0]['m'][0])]
for i,k in enumerate(['PHOENIX-01','PHOENIX-02','PHOENIX-03']):
    s=D[k]['stmt'][0]; D[k]['stmt']=[T('Calculer : {1}', s['x'] if 'x' in s else s['m'][0])]
# bold labels
for e in EX:
    for it in e['sol']:
        if 't' in it:
            it['t']=re.sub(r'^(Limite|Équation|Position) : ',lambda m:'**%s :** '%m.group(1),it['t'])
# R -> \mathbb{R}
def fixm(s):
    s=re.sub(r'^R$',r'\\mathbb{R}',s)
    return s
for e in EX:
    for k in ('stmt','sol'):
        for it in e[k]:
            if 'm' in it: it['m']=[fixm(m) for m in it['m']]
# fill empty lim subscripts from the statement
filled=[]
for e in EX:
    st=' '.join([it['x'] if 'x' in it else ' '.join(it['m']) for it in e['stmt']])
    mm=re.search(r'\\lim_\{([^}]+)\}',st)
    sub=mm.group(1) if mm else None
    for it in e['sol']:
        for key in ('x','m'):
            if key in it:
                vals=[it['x']] if key=='x' else it['m']
                for i,v in enumerate(vals):
                    if r'\lim_{}' in v:
                        assert sub, e['id']
                        sub2=re.sub(r'\s+','',sub).replace(r'\to',r' \to ').replace(r'\infty',r'\infty')
                        v2=v.replace(r'\lim_{}',r'\lim_{%s}'%sub2)
                        filled.append((e['id'],sub2))
                        if key=='x': it['x']=v2
                        else: it['m'][i]=v2
json.dump(EX,open('fr_final.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
print('filled',filled)
# list T items
for e in EX:
    n=0
    print('==',e['id'])
    for k in ('stmt','sol'):
        for j,it in enumerate(e[k]):
            if 't' in it:
                n+=1; print('  %s%d [%d] %s'%(k[0],j,n,it['t']))
