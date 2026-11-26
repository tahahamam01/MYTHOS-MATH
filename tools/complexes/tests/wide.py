import sys,json; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
M="""()=>{document.querySelectorAll('#lw [data-a="view"],#lw [data-a="showc"]').forEach(b=>b.click());return new Promise(r=>setTimeout(()=>r([...document.querySelectorAll('#lw .lwm')].filter(e=>e.scrollWidth>e.clientWidth+3).map(e=>[e.clientWidth,e.scrollWidth,(e.querySelector('annotation')||{}).textContent])),750))}"""
bad=[];n=0
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (1280,390):
        for lg in ('fr','ar'):
            ctx,pg,errs=open_page(b,w,900); pg.evaluate(INIT,[lg,'complexes']); pg.wait_for_timeout(300)
            info=pg.evaluate("()=>window.__T.CH.find(x=>x.id==='complexes').lessons.map(l=>[l.id,l.steps.length])")
            for lid,k in info:
                for st in range(k):
                    pg.evaluate("([l,s])=>window.__T.go('lesson',l,s)",[lid,st]); pg.wait_for_timeout(200); n+=1
                    r=pg.evaluate(M)
                    if r: bad.append((w,lg,lid,st,r))
            pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
            for tier in ['ve','e','m','h','x']:
                cnt=pg.evaluate("(t)=>{const T=window.__T;const c=T.CH.find(x=>x.id==='complexes');return c.exercises.concat(c.optional).filter(i=>T.EXB[i].d===t).length}",tier)
                for i in range(cnt):
                    pg.evaluate("([t,i])=>window.__T.go('exercises',t,i)",[tier,i]); pg.wait_for_timeout(200); n+=1
                    r=pg.evaluate(M)
                    if r: bad.append((w,lg,tier,i,r))
            ctx.close()
    b.close()
import collections
print('pages',n,dict(collections.Counter(x[0] for x in bad)),'pages still overflowing by width')
for x in bad[:12]: print(x[:4],[(a,b_,str(c)[:70]) for a,b_,c in x[4]][:2])
