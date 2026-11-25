import json,sys
from h import *
CHECK="""()=>{const lw=document.querySelector('#lw');if(!lw)return {noLW:1};
const tx=lw.innerText;const o={len:tx.length};
o.kerr=lw.querySelectorAll('.katex-error').length;o.raw=lw.querySelectorAll('.lwraw').length;
o.dollar=(tx.match(/\\$/g)||[]).length;o.bad=/undefined|NaN|\\[object|null/.test(tx);o.star=(tx.match(/\\*\\*|(^|\\s)\\*[^\\s*]/g)||[]).length;
o.hov=document.documentElement.scrollWidth>document.documentElement.clientWidth+2;
o.nk=lw.querySelectorAll('.katex').length;
o.imgbad=[...lw.querySelectorAll('img')].filter(i=>i.complete&&i.naturalWidth===0).length;
o.markers=/\\[R\\d+\\]/.test(tx);o.enonce=/[EÉ]nonc[ée]/.test(tx);return o}"""
res={'lessons':0,'steps':0,'ex':0,'issues':[]}
with sync_playwright() as p:
    b=p.chromium.launch()
    for (w,h) in [(1280,900),(390,844)]:
      for lg in ['fr','en','ar']:
        ctx,pg,errs=open_page(b,w,h)
        pg.evaluate(INIT,[lg,'suites']); pg.wait_for_timeout(300)
        info=pg.evaluate("()=>{const T=window.__T;const c=T.CH.find(x=>x.id==='suites');return {les:c.lessons.map(l=>[l.id,l.steps.length]),ex:c.exercises}}")
        for lid,n in info['les']:
            for st in range(n):
                pg.evaluate("([l,s])=>{const T=window.__T;T.go('lesson',l,s)}",[lid,st]); pg.wait_for_timeout(260)
                r=pg.evaluate(CHECK); res['steps']+=1
                if r.get('noLW') or r['len']<20 or r['kerr'] or r['raw'] or r['dollar'] or r['bad'] or r['star'] or r['hov'] or r['imgbad'] or r['markers'] or r['enonce']:
                    res['issues'].append([w,lg,'lesson',lid,st,r])
        pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
        for tier in ['ve','e','m','h','x']:
            pg.evaluate("(t)=>{const T=window.__T;T.go('exercises',t,0)}",tier); pg.wait_for_timeout(260)
            cnt=pg.evaluate("(t)=>{const T=window.__T;return T.CH.find(x=>x.id==='suites').exercises.filter(i=>T.EXB[i]&&T.EXB[i].d===t).length}",tier)
            for i in range(cnt):
                pg.evaluate("([t,i])=>{const T=window.__T;T.go('exercises',t,i)}",[tier,i]); pg.wait_for_timeout(260)
                r=pg.evaluate(CHECK); res['ex']+=1
                if r.get('noLW') or r['len']<15 or r['kerr'] or r['raw'] or r['dollar'] or r['bad'] or r['star'] or r['hov'] or r['imgbad'] or r['markers']:
                    res['issues'].append([w,lg,'ex',tier,i,r])
        res.setdefault('pageerrs',{})[f'{w}-{lg}']=[e for e in errs if 'createClient' not in e]
        ctx.close()
    b.close()
print(json.dumps({k:v for k,v in res.items() if k!='issues'},ensure_ascii=False)); print(len(res['issues']))
json.dump(res['issues'],open('issues.json','w'),ensure_ascii=False)
for i in res['issues'][:25]: print(i)
