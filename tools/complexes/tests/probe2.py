import sys,json; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
M="""()=>[...document.querySelectorAll('#lw .lwm')].map(e=>{const k=e.querySelector('.katex-html');const cw=e.clientWidth-0;const w=k?k.getBoundingClientRect().width:0;const fs=parseFloat(getComputedStyle(e.querySelector('.katex')).fontSize);return [Math.round(cw),Math.round(w),fs,(e.querySelector('annotation')||{}).textContent]}).filter(a=>a[1]>a[0])"""
out=[]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900)
    pg.evaluate(INIT,['fr','complexes']); pg.wait_for_timeout(300)
    info=pg.evaluate("()=>window.__T.CH.find(x=>x.id==='complexes').lessons.map(l=>[l.id,l.steps.length])")
    for lid,n in info:
        for st in range(n):
            pg.evaluate("([l,s])=>window.__T.go('lesson',l,s)",[lid,st]); pg.wait_for_timeout(200)
            pg.evaluate("()=>document.querySelectorAll('#lw [data-a=\"view\"]').forEach(b=>b.click())")
            for a in pg.evaluate(M): out.append(('L',lid,st)+tuple(a))
    pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
    for tier in ['ve','e','m','h','x']:
        cnt=pg.evaluate("(t)=>{const T=window.__T;const c=T.CH.find(x=>x.id==='complexes');return c.exercises.concat(c.optional).filter(i=>T.EXB[i].d===t).length}",tier)
        for i in range(cnt):
            pg.evaluate("([t,i])=>window.__T.go('exercises',t,i)",[tier,i]); pg.wait_for_timeout(200)
            for a in pg.evaluate(M): out.append(('E',tier,i)+tuple(a))
    b.close()
print(len(out),'overflowing display equations of ~',)
import collections
need=[round(a[4]/a[3],2) for a in out]  # width/clientwidth
print(sorted(need)[-15:])
print(sum(1 for n in need if n<=1.15),'would fit at 1.15x smaller ;',sum(1 for n in need if n<=1.35),'at ~1.35x smaller')
for a in out[:12]: print(a[:6],str(a[7])[:90].replace('\n',' '))
