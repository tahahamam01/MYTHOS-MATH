import json,sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
CH_='complexes'
CHECK="""()=>{const lw=document.querySelector('#lw');if(!lw)return {noLW:1};
document.querySelectorAll('#lw [data-a="view"],#lw [data-a="showc"]').forEach(b=>b.click());
const tx=lw.innerText;const o={len:tx.length};
o.kerr=lw.querySelectorAll('.katex-error').length;o.raw=lw.querySelectorAll('.lwraw').length;
o.dollar=(tx.match(/\\$/g)||[]).length;o.bad=/undefined|NaN|\\[object|null/.test(tx);o.star=(tx.match(/\\*/g)||[]).length;
o.ib=tx.includes('\\u2062');o.hov=document.documentElement.scrollWidth>document.documentElement.clientWidth+2;
o.nk=lw.querySelectorAll('.katex').length;
o.imgbad=[...lw.querySelectorAll('img')].filter(i=>i.offsetParent&&i.complete&&i.naturalWidth===0).length;
o.imgvis=[...lw.querySelectorAll('.coimg img')].filter(i=>i.offsetParent).length;
o.wide=[...lw.querySelectorAll('.lwm')].filter(e=>e.scrollWidth>e.clientWidth+3).length;
o.corr=lw.querySelectorAll('.lwc').length;return o}"""
res={'steps':0,'ex':0,'issues':[],'imgs':0,'pageerrs':{}}
with sync_playwright() as p:
    b=p.chromium.launch()
    for (w,h) in [(1280,900),(390,844)]:
      for lg in ['fr','en','ar']:
        for th in ['light','dark']:
            if w==390 and th=='light': continue
            ctx,pg,errs=open_page(b,w,h)
            pg.evaluate(INIT,[lg,CH_]); pg.wait_for_timeout(300)
            pg.evaluate("t=>{document.documentElement.dataset.theme=t}",th)
            info=pg.evaluate("()=>{const T=window.__T;const c=T.CH.find(x=>x.id==='complexes');return {les:c.lessons.map(l=>[l.id,l.steps.length])}}")
            def chk(kind,a,b_):
                pg.wait_for_timeout(520); pg.evaluate("t=>{document.documentElement.dataset.theme=t}",th)
                r=pg.evaluate(CHECK); res['imgs']+=r.get('imgvis',0)
                if r.get('noLW') or r['len']<15 or r['kerr'] or r['raw'] or r['dollar'] or r['bad'] or r['star'] or r['ib'] or r['hov'] or r['imgbad'] or r['wide']:
                    res['issues'].append([w,lg,th,kind,a,b_,r])
            for lid,n in info['les']:
                for st in range(n):
                    pg.evaluate("([l,s])=>window.__T.go('lesson',l,s)",[lid,st]); chk('lesson',lid,st); res['steps']+=1
            pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
            for tier in ['ve','e','m','h','x']:
                cnt=pg.evaluate("(t)=>{const T=window.__T;return T.CH.find(x=>x.id==='complexes').exercises.concat(T.CH.find(x=>x.id==='complexes').optional||[]).filter(i=>T.EXB[i]&&T.EXB[i].d===t).length}",tier)
                for i in range(cnt):
                    pg.evaluate("([t,i])=>window.__T.go('exercises',t,i)",[tier,i]); chk('ex',tier,i); res['ex']+=1
            res['pageerrs'][f'{w}-{lg}-{th}']=[e for e in errs if 'createClient' not in e][:3]
            ctx.close()
    b.close()
print(json.dumps({k:v for k,v in res.items() if k!='issues'},ensure_ascii=False)); print('issues',len(res['issues']))
json.dump(res['issues'],open('/tmp/claude-0/-home-claude/1172a3da-d14e-52ac-ae2c-05145723c309/scratchpad/issues.json','w'),ensure_ascii=False)
for i in res['issues'][:20]: print(i)
