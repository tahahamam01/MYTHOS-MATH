import sys,json,re,copy
sys.path.insert(0,'/home/claude/work')
import importlib,mathconv; importlib.reload(mathconv)
from mathconv import conv

PRE=[
("lim f(x)/x = ±∞","$\\lim_{x\\to+\\infty}\\dfrac{f(x)}{x}=\\pm\\infty$"),
("lim f(x)/x = 0","$\\lim_{x\\to+\\infty}\\dfrac{f(x)}{x}=0$"),
("lim f(x)/x = a","$\\lim_{x\\to+\\infty}\\dfrac{f(x)}{x}=a$"),
("lim [f(x) − ax] = ±∞","$\\lim_{x\\to+\\infty}\\left[f(x)-ax\\right]=\\pm\\infty$"),
("lim [f(x) − (ax + b)] = 0","$\\lim\\left[f(x)-(ax+b)\\right]=0$"),
("lim f(x) = ±∞","$\\lim f(x)=\\pm\\infty$"),
("lim f(x) = L","$\\lim f(x)=L$"),
("f(milieu) < 0 → α est à droite du milieu ; f(milieu) > 0 → α est à gauche","$f(\\text{milieu})<0$ → $\\alpha$ est à droite du milieu ; $f(\\text{milieu})>0$ → $\\alpha$ est à gauche"),
("f(midpoint) < 0 → α is to the right of the midpoint; f(midpoint) > 0 → α is to the left","$f(\\text{midpoint})<0$ → $\\alpha$ is to the right of the midpoint; $f(\\text{midpoint})>0$ → $\\alpha$ is to the left"),
("donc y x² + y = x²","donc $yx^{2}+y=x^{2}$"),("so y x² + y = x²","so $yx^{2}+y=x^{2}$"),("the y-axis","the $y$-axis"),
("nombre a**","nombre $a$**"),("part de a sur","part de $a$ sur"),("nombre b**","nombre $b$**"),("part de b sur","part de $b$ sur"),
("abscisse a.","abscisse $a$."),("tangente en a est","tangente en $a$ est"),("verticale en a :","verticale en $a$ :"),("dérivable en a,","dérivable en $a$,"),("dérivable en a (ex","dérivable en $a$ (ex"),
("tend vers a.","tend vers $a$."),("(a réel non nul)","($a$ réel non nul)"),("solution** c dans","solution** $c$ dans"),("Déterminer a et b","Déterminer $a$ et $b$"),
("number a**","number $a$**"),("start from a on","start from $a$ on"),("number b**","number $b$**"),("start from b on","start from $b$ on"),
("abscissa a.","abscissa $a$."),("tangent at a is","tangent at $a$ is"),("tangent at a:","tangent at $a$:"),("differentiable at a,","differentiable at $a$,"),("differentiable at a (e.g.","differentiable at $a$ (e.g."),
("tends to a.","tends to $a$."),("(a a nonzero real)","($a$ a nonzero real)"),("solution** c in","solution** $c$ in"),("Determine a and b","Determine $a$ and $b$"),
]
CELL=re.compile(r'[−+∞\d,.\s↗↘‖∅]*|\$[^$]*\$')
def tx(o):
    for k in ('fr','en'):
        if isinstance(o.get(k),str):
            v=o[k]
            for a,c in PRE: v=v.replace(a,c)
            o[k]=conv(v,k)
def walk(o):
    if isinstance(o,dict):
        if 'dtab' in o:
            for lk in o['dtab']:
                if isinstance(o['dtab'][lk],list):
                    o['dtab'][lk]=[[ (c if CELL.fullmatch(c or '') else conv(c,'fr' if lk=='fr' else 'en')) for c in row] for row in o['dtab'][lk]]
            return
        if 'fr' in o and isinstance(o['fr'],str): tx(o)
        for k,v in o.items():
            if k not in('fr','en','img'): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
def run(d):
    new=copy.deepcopy(d)
    for e in new['EX']:
        if e['d'] in('ve','e','m'): walk(e)
    for l in (1,3,4): walk(new['LES'][l])
    for a in new['APPS']: walk(a)
    return new
def allstrs(o,res):
    if isinstance(o,dict):
        for v in o.values(): allstrs(v,res)
    elif isinstance(o,list):
        for v in o: allstrs(v,res)
    elif isinstance(o,str): res.append(o)
if __name__=='__main__':
    d=json.load(open('/home/claude/data.json')); new=run(d)
    json.dump(new,open('/home/claude/data_new.json','w'),ensure_ascii=False,indent=1)
    res=[];allstrs(new,res); json.dump(res,open('/home/claude/allstrs.json','w'),ensure_ascii=False)
