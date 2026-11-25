import re,collections
from h import *
TXT="""()=>{const c=document.querySelector('#lw').cloneNode(true);c.querySelectorAll('.katex,.katex-display,nav,.lwng,button').forEach(e=>e.remove());return c.innerText}"""
FRW=re.compile(r"\b(le|la|les|des|est|une|donc|alors|pour|dans|que|sur|avec|soit|puisque|on|calculer|montrer)\b",re.I)
res=collections.Counter();ex=collections.defaultdict(set)
with sync_playwright() as p:
    b=p.chromium.launch()
    for lg in ['ar','en']:
        ctx,pg,errs=open_page(b,1280,900); pg.evaluate(INIT,[lg,'suites'])
        info=pg.evaluate("()=>{const c=window.__T.CH.find(x=>x.id==='suites');return c.lessons.map(l=>[l.id,l.steps.length])}")
        pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
        pages=[('lesson',l,i) for l,n in info for i in range(n)]
        for t in ['ve','e','m','h','x']:
            cnt=pg.evaluate("(t)=>{const T=window.__T;return T.CH.find(x=>x.id==='suites').exercises.filter(i=>T.EXB[i].d===t).length}",t)
            pages+=[('ex',t,i) for i in range(cnt)]
        for k,a,i in pages:
            pg.evaluate("([k,a,i])=>{const T=window.__T;k==='lesson'?T.go('lesson',a,i):T.go('exercises',a,i)}",[k,a,i]); pg.wait_for_timeout(60)
            t=pg.evaluate(TXT)
            if lg=='ar':
                bad=[w for w in re.findall(r"[A-Za-zÀ-ÿ]{3,}",t) if w.lower() not in ("chick","chicken","raven","eagle","phoenix","télescopage")]
                if bad: res['ar']+=1; ex['ar'].add((k,a,i,' '.join(bad[:5])))
            else:
                bad=FRW.findall(t); acc=re.findall(r"[àâçéèêëîïôùûœ]",t)
                if len(bad)>3 or acc: res['en']+=1; ex['en'].add((k,a,i,' '.join(bad[:4]),''.join(acc[:5])))
        ctx.close()
    b.close()
print(dict(res))
for l in ex: print(l,sorted(ex[l])[:12])
