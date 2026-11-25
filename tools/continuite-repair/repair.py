import sys,json,re,copy
sys.path.insert(0,'/home/claude/work')
import build_data
SRC='/home/claude/mythos-math/backup/index.before-continuite-repair.html'
OUT='/home/claude/mythos-math/index.html'
s=open(SRC,encoding='utf8').read()
def grab(name):
    i=s.index('const '+name+'=',949000)+len('const '+name+'=')
    j=s.index('\n',i); return i,j,json.loads(s[i:j-1])
(iL,jL,LES),(iA,jA,APPS),(iE,jE,EX)=grab('COLES'),grab('COAPPS'),grab('COEX')
# round-trip check
dump=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
for nm,(i,j,o) in dict(L=(iL,jL,LES),A=(iA,jA,APPS),E=(iE,jE,EX)).items():
    assert dump(o)==s[i:j-1],'roundtrip mismatch '+nm
d=build_data.run(dict(LES=LES,APPS=APPS,EX=EX))
LES,APPS,EX=d['LES'],d['APPS'],d['EX']
byid={e['id']:e for e in EX}
# ---- 3. CHICK statements
def T(fr,en): return {'fr':fr,'en':en}
M=lambda x:x
CH={
'co-chick-01':(T("Soit $f(x)=x^{2}-3$ et $\\alpha$ la solution positive de l’équation $f(x)=0$, située dans $[1\\,;\\,2]$. Par dichotomie, donner un encadrement de $\\alpha$ d’amplitude $0{,}25$.","Let $f(x)=x^{2}-3$ and let $\\alpha$ be the positive solution of $f(x)=0$, lying in $[1\\,;\\,2]$. By dichotomy, give a bracketing of $\\alpha$ of width $0.25$."),[]),
'co-chick-02':(T("Soit $f(x)=x+3$ définie sur $\\mathbb{R}$. Montrer que $f$ admet une fonction réciproque $f^{-1}$ et la déterminer.","Let $f(x)=x+3$ defined on $\\mathbb{R}$. Show that $f$ has an inverse function $f^{-1}$ and determine it."),[]),
'co-chick-03':(T("Soit $f(x)=3x-2$ définie sur $\\mathbb{R}$. Déterminer la fonction réciproque $f^{-1}$ de $f$ et son ensemble de définition.","Let $f(x)=3x-2$ defined on $\\mathbb{R}$. Determine the inverse function $f^{-1}$ of $f$ and its domain."),[]),
'co-chick-04':(T("Soit $f(x)=x^{2}+1$ définie sur $[0\\,;\\,+\\infty[$. Montrer que $f$ admet une fonction réciproque et la déterminer, avec son ensemble de définition.","Let $f(x)=x^{2}+1$ defined on $[0\\,;\\,+\\infty[$. Show that $f$ has an inverse function and determine it, together with its domain."),[]),
'co-chick-05':(T("Soit $f(x)=x^{3}-1$ définie sur $\\mathbb{R}$. Déterminer la fonction réciproque $f^{-1}$ de $f$, puis vérifier le résultat en calculant $f(f^{-1}(x))$.","Let $f(x)=x^{3}-1$ defined on $\\mathbb{R}$. Determine the inverse function $f^{-1}$ of $f$, then check the result by computing $f(f^{-1}(x))$."),[]),
'co-chick-06':(T("Montrer, à l’aide du TVI, que l’équation $x^{2}=5$ admet au moins une solution dans $[2\\,;\\,3]$. (On pourra poser $f(x)=x^{2}-5$.)","Using the IVT, show that the equation $x^{2}=5$ has at least one solution in $[2\\,;\\,3]$. (You may set $f(x)=x^{2}-5$.)"),[]),
'co-chick-07':(T("Montrer que l’équation $x^{3}+2x=4$ admet une solution unique dans $[1\\,;\\,2]$. (On pourra poser $f(x)=x^{3}+2x-4$.)","Show that the equation $x^{3}+2x=4$ has a unique solution in $[1\\,;\\,2]$. (You may set $f(x)=x^{3}+2x-4$.)"),[]),
'co-chick-08':(T("Montrer que l’équation $\\sqrt{x}+x=4$ admet une solution unique dans $[1\\,;\\,4]$. (On pourra poser $f(x)=\\sqrt{x}+x-4$.)","Show that the equation $\\sqrt{x}+x=4$ has a unique solution in $[1\\,;\\,4]$. (You may set $f(x)=\\sqrt{x}+x-4$.)"),[]),
'co-chick-09':(T("Montrer que l’équation $x^{2}+x=7$ admet une solution unique dans $[2\\,;\\,3]$. (On pourra poser $f(x)=x^{2}+x-7$.)","Show that the equation $x^{2}+x=7$ has a unique solution in $[2\\,;\\,3]$. (You may set $f(x)=x^{2}+x-7$.)"),[]),
'co-chick-10':(T("Soit $f(x)=x^{3}+x$.","Let $f(x)=x^{3}+x$."),[
 T("1. Montrer que $f$ est continue et strictement croissante sur $\\mathbb{R}$.","1. Show that $f$ is continuous and strictly increasing on $\\mathbb{R}$."),
 T("2. Montrer que l’équation $f(x)=3$ admet une solution unique $\\alpha$ dans $[1\\,;\\,2]$.","2. Show that the equation $f(x)=3$ has a unique solution $\\alpha$ in $[1\\,;\\,2]$."),
 T("3. Par dichotomie, donner un encadrement de $\\alpha$ d’amplitude $0{,}25$.","3. By dichotomy, give a bracketing of $\\alpha$ of width $0.25$."),
 T("4. Justifier que $f$ admet une fonction réciproque $f^{-1}$. Comment sont placées les courbes de $f$ et de $f^{-1}$ ?","4. Justify that $f$ has an inverse function $f^{-1}$. How are the curves of $f$ and $f^{-1}$ placed?")])}
MSG='Cette série ne contient que des corrigés'
for k,(p,bl) in CH.items():
    e=byid[k]; assert e['p']['fr'].startswith(MSG),k
    e['p']=p
    if bl: e['blocks']=bl
assert not any(MSG in e['p']['fr'] for e in EX)
# ---- 4. Eagle 15
e=byid['co-eagle-15']; assert 'synth' in e['p']['fr']
e['p']={'fr':'**Exercice 15 : Le problème de synthèse**','en':'**Exercise 15: The synthesis problem**'}
# ---- 5/6. Phoenix
e=byid['co-phoenix-01']
assert 'itérée' in e['p']['fr']
e['p']={'fr':'**$f(x)=x^{3}-3x$**','en':'**$f(x)=x^{3}-3x$**'}
bl=e['blocks']
for b in bl:
    if b['fr']=='**Partie B : le comptage monstrueux**': b['fr']='**Partie B : Dénombrement des solutions**'; b['en']='**Part B: Counting the solutions**'; nb=1
    if b['fr']=='**Partie D : le boss final**': b['fr']='**Partie D : Solutions de l’équation $f^{2}(x)=x$**'; b['en']='**Part D: Solutions of the equation $f^{2}(x)=x$**'; nd=1
assert nb and nd
# ---- figure 1 move (s5)
st=[x for x in LES[1]['steps'] if x['id']=='s5'][0]['blocks']
ii=[i for i,b in enumerate(st) if 'img' in b][0]; img=st.pop(ii)
ex=[i for i,b in enumerate(st) if 'fr' in b and b['fr'].startswith('**Exemple.**')][0]
cap=[i for i,b in enumerate(st) if 'fr' in b and b['fr'].startswith('Figure :')][0]
capb=st.pop(cap)
ex=[i for i,b in enumerate(st) if 'fr' in b and b['fr'].startswith('**Exemple.**')][0]
st.insert(ex+1,img); st.insert(ex+2,capb)
# ---- write
new=s[:iL]+dump(LES)+s[jL-1:iA]+dump(APPS)+s[jA-1:iE]+dump(EX)+s[jE-1:]
# apps/les/ex are in different order in file: rebuild safely by position
parts=sorted([(iL,jL,LES),(iA,jA,APPS),(iE,jE,EX)])
out=[];pos=0
for i,j,o in parts:
    out.append(s[pos:i]); out.append(dump(o)); pos=j-1
out.append(s[pos:]); new=''.join(out)
exec(open('/home/claude/work/figures.py').read())
open(OUT,'w',encoding='utf8').write(new)
print('written',len(new))
