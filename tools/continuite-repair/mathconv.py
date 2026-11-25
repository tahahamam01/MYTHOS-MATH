import re
SUPM={'²':'2','³':'3','¹':'1','⁰':'0','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','ⁿ':'n','⁺':'+','⁻':'-'}
SUBM={'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9'}
GREEK='αβγδεθλμπρστφωΔΩΣ'
GL={'α':r'\alpha','β':r'\beta','γ':r'\gamma','δ':r'\delta','ε':r'\varepsilon','θ':r'\theta','λ':r'\lambda','μ':r'\mu','π':r'\pi','ρ':r'\rho','σ':r'\sigma','τ':r'\tau','φ':r'\varphi','ω':r'\omega','Δ':r'\Delta','Ω':r'\Omega','Σ':r'\Sigma'}
SYM={'ℝ':r'\mathbb{R}','∞':r'\infty','∅':r'\varnothing','≤':r'\leq','≥':r'\geq','≠':r'\neq','≈':r'\approx','∈':r'\in','∪':r'\cup','∩':r'\cap','→':r'\to','↗':r'\nearrow','↘':r'\searrow','×':r'\times','·':r'\cdot','−':'-','+':'+','=':'=','<':'<','>':'>','↦':r'\mapsto','⇒':r'\Rightarrow','⟹':r'\Rightarrow','⇔':r'\iff','±':r'\pm','…':r'\ldots','∖':r'\setminus','\\':r'\setminus','|':'|','‖':r'\Vert'}
OPS=set('+−±=<>≤≥≠≈∈∪∩→↗↘×·/↦⇒⟹⇔∖\\')
REL=set('=<>≤≥≠≈∈→↦⇒⟹⇔↗↘')
PUA0=0xE000
MATHWORDS={'lim':r'\lim','ln':r'\ln','exp':r'\exp','sin':r'\sin','cos':r'\cos'}
WRAPVARS=set('fghxkmnIJO')|set(GREEK)
TOK=re.compile(r"""(?P<BOLD>\*\*)|(?P<ABBR>\b[eEiI]\.[geGE]\.)|(?P<ELI>[A-Za-zÀ-ÿ]['’](?=[A-Za-zÀ-ÿ]))|(?P<OXY>\bO[xy]\b)|(?P<WORD>[A-Za-zÀ-ÿ]{2,})|(?P<NUM>\d+(?:[.,]\d+)?)|(?P<LET>[A-Za-z%s])|(?P<SUP>[²³¹⁰⁴⁵⁶⁷⁸⁹ⁿ⁺⁻]+)|(?P<SUB>[₀-₉]+)|(?P<PUA>[\uE000-\uE0FF])|(?P<SP>[\s\u00a0\u202f]+)|(?P<OTH>.)""" % GREEK,re.S)
def tokenize(s):
    out=[]
    for m in TOK.finditer(s):
        k=m.lastgroup; t=m.group()
        if k=='WORD' and t in MATHWORDS: k='MW'
        if k=='WORD' and t in ('ax','bx','kx'): k='ID'
        if k=='OXY': k='LET2'
        out.append((k,t))
    return out
def ismath(k,t,depth):
    if k in('LET','NUM','SUP','SUB','PUA','MW','LET2','ID'): return True
    if k=='OTH':
        if t in OPS or t in SYM or t in '()[]√∛^_\'’{}…': return True
        if t in ';,' and depth>0: return True
        if t=='-' : return False
        return False
    return False
def split_runs(toks):
    """return list of (is_math, [tokens])"""
    res=[];i=0;n=len(toks);cur=None;depth=0
    def flush():
        nonlocal cur
        if cur: res.append((True,cur)); cur=None
    plain=[]
    while i<n:
        k,t=toks[i]
        if k=='SP':
            # decide inclusion
            if cur:
                j=i+1
                nxt=toks[j] if j<n else None
                prv=cur[-1]
                if nxt and ismath(nxt[0],nxt[1],depth) and ((prv[0]=='OTH' and (prv[1] in OPS or prv[1] in '([;,' )) or (nxt[0]=='OTH' and (nxt[1] in OPS or nxt[1] in ')];,' or nxt[1] in '^_')) ):
                    cur.append((k,' ')); i+=1; continue
                flush()
            res.append((False,[(k,t)])); i+=1; continue
        if ismath(k,t,depth):
            if k=='OTH' and t in '([': depth+=1
            if k=='OTH' and t in ')]': depth=max(0,depth-1)
            if cur is None: cur=[]
            cur.append((k,t)); i+=1; continue
        flush(); depth=0
        res.append((False,[(k,t)])); i+=1
    flush()
    return res

class P:
    def __init__(s,toks,lang,ph):
        s.t=[x for x in toks if x[0]!='SP']; s.i=0; s.lang=lang; s.ph=ph
        # merge primes
    def peek(s,o=0):
        j=s.i+o
        return s.t[j] if j<len(s.t) else (None,None)
    def num(s,t):
        if s.lang=='fr': return t.replace(',','{,}').replace('.','{,}')
        return t.replace(',','{,}')
    def atom(s):
        k,t=s.peek()
        if k=='LET':
            s.i+=1; return GL.get(t,t)
        if k=='LET2': s.i+=1; return r'\mathrm{%s}'%t if False else t
        if k=='MW': s.i+=1; return MATHWORDS[t]
        if k=='ID': s.i+=1; return t
        if k=='NUM': s.i+=1; return s.num(t)
        if k=='PUA': s.i+=1; return s.ph[ord(t)-PUA0]
        if k=='OTH' and t in 'ℝ∞∅|‖': s.i+=1; return SYM[t]
        if k=='OTH' and t=='{': s.i+=1; return r'\{'
        if k=='OTH' and t=='}': s.i+=1; return r'\}'
        return None
    def group(s):
        k,t=s.peek(); close={'(':')','[':']'}[t]; s.i+=1
        inner=s.seq(close); 
        k2,t2=s.peek()
        if t2==close: s.i+=1
        return t,inner,close
    def render_group(s,o,inner,c):
        if r'\dfrac' in inner: return r'\left%s %s\right%s'%(o,inner,c)
        return o+inner+c
    def postfix(s,lat):
        while True:
            k,t=s.peek()
            if k=='OTH' and t in "'’":
                s.i+=1; lat+="'"; continue
            if k=='SUP':
                m=''.join(SUPM[c] for c in t); s.i+=1; lat+='^{%s}'%m; continue
            if k=='SUB':
                m=''.join(SUBM[c] for c in t); s.i+=1; lat+='_{%s}'%m; continue
            if k=='OTH' and t=='^':
                s.i+=1; k2,t2=s.peek()
                if t2=='(':
                    o,inner,c=s.group(); lat+='^{%s}'%inner.replace(r'\dfrac',r'\frac')
                else:
                    a=s.atom() ; lat+='^{%s}'%a
                continue
            if k=='OTH' and t=='_':
                s.i+=1; a=s.atom(); lat+='_{%s}'%a; continue
            break
        return lat
    def primary(s):
        k,t=s.peek()
        if k is None: return None
        if k=='OTH' and t in '√∛':
            s.i+=1; k2,t2=s.peek(); ix='[3]' if t=='∛' else ''
            if t2=='(':
                o,inner,c=s.group(); lat=r'\sqrt%s{%s}'%(ix,inner)
            else:
                a=s.atom()
                if a is None: return None
                lat=r'\sqrt%s{%s}'%(ix,a)
            return (s.postfix(lat),None)
        if k=='OTH' and t in '([':
            o,inner,c=s.group()
            l0=s.render_group(o,inner,c); l1=s.postfix(l0)
            return (l1, inner if l1==l0 else None)
        a=s.atom()
        if a is None: return None
        lat=a
        lat=s.postfix(lat)
        k2,t2=s.peek()
        if k in('LET','MW') and k2=='OTH' and t2=='(':
            o,inner,c=s.group(); lat=s.postfix(lat+s.render_group(o,inner,c))
        return (lat,None)
    def chunk(s):
        prims=[]
        while True:
            save=s.i
            p=s.primary()
            if p is None: s.i=save; break
            prims.append(p)
            k,t=s.peek()
            if k=='OTH' and t=='/':
                s.i+=1
                d=s.primary()
                if d is None:
                    prims.append(('/',None)); break
                num=prims[0][1] if (len(prims)==1 and prims[0][1] is not None) else ''.join(x[0] for x in prims)
                den=d[1] if d[1] is not None else d[0]
                prims=[(r'\dfrac{%s}{%s}'%(num,den),None)]
        return ''.join(x[0] for x in prims)
    def seq(s,close=None):
        out=[]
        while True:
            k,t=s.peek()
            if k is None: break
            if close and k=='OTH' and t==close: break
            if k=='OTH' and t in ')]' and not close: out.append(t); s.i+=1; continue
            c=s.chunk()
            if c: out.append(c); continue
            if k=='OTH':
                s.i+=1
                if t in SYM and t not in 'ℝ∞∅|‖': out.append(SYM[t])
                elif t==';': out.append(r'\,;\,')
                elif t==',': out.append(',')
                elif t in ')]': out.append(t)
                elif t in '([': out.append(t)
                elif t in "'’": out.append("'")
                elif t=='/': out.append('/')
                else: out.append(t)
                continue
            s.i+=1; out.append(t)
        return join(out)
def join(parts):
    r=''
    for p in parts:
        if r and re.search(r'\\[A-Za-z]+$',r) and re.match(r'[A-Za-z0-9]',p): r+=' '
        r+=p
    return r
PHRE=re.compile(r"([\[\]\(])([^\[\]()\n;]{1,45}?)[ \u00a0\u202f]*;[ \u00a0\u202f]*([^\[\]()\n;]{1,45}?)([\[\]\)])")
SIDE=re.compile(r"^[\sA-Za-z0-9_−+\-∞,./√²³⁻⁺ⁿ'’αβγℝ]*$")
def protect(s,lang,ph):
    def rep(m):
        a,b=m.group(2),m.group(3)
        for x in (a,b):
            if not x.strip() or not SIDE.match(x) or re.search(r'[A-Za-z]{2,}',x): return m.group(0)
        la=run_latex(tokenize(a.strip()),lang,ph); lb=run_latex(tokenize(b.strip()),lang,ph)
        ph.append(m.group(1)+la+r'\,;\,'+lb+m.group(4))
        return chr(PUA0+len(ph)-1)
    return PHRE.sub(rep,s)
def run_latex(toks,lang,ph):
    p=P(toks,lang,ph); return p.seq()
def meaningful(toks,prevword):
    ks=[(k,t) for k,t in toks if k!='SP']
    if not ks: return False
    if len(ks)==1:
        k,t=ks[0]
        if k=='LET': return t in WRAPVARS and not(t=='y' and prevword.lower()=='il')
        if k=='NUM': return bool(re.search(r'[.,]',t))
        if k=='PUA': return True
        if k=='OTH': return t in 'ℝ∞∅↗↘∩∪'
        if k in('MW','LET2','ID'): return True
        return False
    for k,t in ks:
        if k in('LET','MW','PUA','SUP','SUB','LET2','ID'): return True
        if k=='OTH' and (t in OPS or t in 'ℝ∞∅√∛|'): return True
        if k=='NUM' and re.search(r'[.,]',t): return True
    return False
def trim(run):
    r=list(run)
    changed=True
    while changed:
        changed=False
        while r and r[0][0]=='SP': r.pop(0)
        while r and r[-1][0]=='SP': r.pop()
        if not r: break
        # unbalanced parens
        txt=[t for k,t in r if k=='OTH']
        if r[0]==('OTH',')') or r[0]==('OTH',']') and txt.count(']')>txt.count('[') and False: r.pop(0); changed=True; continue
        if r[-1]==('OTH','('): r.pop(); changed=True; continue
        op=sum(1 for k,t in r if k=='OTH' and t=='('); cp=sum(1 for k,t in r if k=='OTH' and t==')')
        if cp>op and r[-1]==('OTH',')'): r.pop(); changed=True; continue
        if op>cp and r[0]==('OTH','('): r.pop(0); changed=True; continue
        # dangling binary ops
        if r[-1][0]=='OTH' and r[-1][1] in OPS and len(r)>1 and r[-1][1] not in '−+±': pass
        if r[-1][0]=='OTH' and r[-1][1] in OPS: r.pop(); changed=True; continue
        if r[0][0]=='OTH' and r[0][1] in OPS and r[0][1] not in '−+±': r.pop(0); changed=True; continue
        if r[0][0]=='OTH' and r[0][1] in '−+±' and (len(r)==1): r.pop(0); changed=True; continue
    return r
def conv_plain(s,lang):
    ph=[]
    s=protect(s,lang,ph)
    toks=tokenize(s)
    out=[];prevword=''
    for ism,run in split_runs(toks):
        if not ism:
            k,t=run[0]
            if k in('WORD','ELI'): prevword=t
            out.append(t if k!='PUA' else t); continue
        # trim: keep leading/trailing removed tokens as plain
        r=trim(run)
        # recompute leading/trailing plain text
        txt_all=''.join(t for k,t in run)
        txt_core=''.join(t for k,t in r)
        idx=txt_all.find(txt_core) if txt_core else -1
        if not r or idx<0 or not meaningful(r,prevword):
            out.append(txt_all); continue
        lat=run_latex(r,lang,ph)
        out.append(txt_all[:idx]+'$'+lat+'$'+txt_all[idx+len(txt_core):])
    res=''.join(out)
    for i,x in enumerate(ph): res=res.replace(chr(PUA0+i),x)  # leftover placeholders (non-wrapped)
    return res
def conv(s,lang):
    s=s.replace('\\|','|')
    parts=re.split(r'(\$[^$]*\$)',s)
    return ''.join(p if (i%2) else conv_plain(p,lang) for i,p in enumerate(parts))
