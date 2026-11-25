import json,sys
sys.path.insert(0,'/home/claude/w/m19/mythos-math/tools/suites/tests')
from h import *
CHECK="""()=>{const lw=document.querySelector('#lw');if(!lw)return {noLW:1};const tx=lw.innerText;const o={len:tx.length};
o.kerr=lw.querySelectorAll('.katex-error').length;o.dollar=(tx.match(/\\$/g)||[]).length;o.bad=/undefined|NaN|\\[object|null/.test(tx);
o.star=(tx.match(/\\*\\*/g)||[]).length;o.hov=document.documentElement.scrollWidth>document.documentElement.clientWidth+2;
o.imgs=lw.querySelectorAll('img').length;o.vis=[...lw.querySelectorAll('img')].filter(i=>i.offsetParent!==null).length;
o.imgbad=[...lw.querySelectorAll('img')].filter(i=>i.offsetParent!==null&&i.complete&&i.naturalWidth===0).length;
o.edit=/inferred|AI\\/|front-end|Implementation/.test(tx);return o}"""
res={'steps':0,'issues':[],'figs':0}
with sync_playwright() as p:
    b=p.chromium.launch()
    for (w,h) in [(1280,900),(390,844)]:
      for lg in ['fr','en','ar']:
        ctx,pg,errs=open_page(b,w,h)
        pg.evaluate(INIT,[lg,'trace']); pg.wait_for_timeout(300)
        info=pg.evaluate("()=>window.__T.CH.find(x=>x.id==='trace').lessons.map(l=>[l.id,l.steps.length])")
        for lid,n in info:
            for st in range(n):
                pg.evaluate("([l,s])=>window.__T.go('lesson',l,s)",[lid,st]); pg.wait_for_timeout(250)
                r=pg.evaluate(CHECK); res['steps']+=1; res['figs']+=r.get('vis',0)
                if r.get('noLW') or r['len']<20 or r['kerr'] or r['dollar'] or r['bad'] or r['star'] or r['hov'] or r['imgbad'] or r['edit'] or r['imgs']!=2*r['vis']:
                    res['issues'].append([w,lg,lid,st,r])
        res.setdefault('errs',{})[f'{w}-{lg}']=[e for e in errs if 'createClient' not in e][:2]
        if w==1280 and lg=='fr': pg.evaluate("()=>window.__T.go('lesson','tr-l4',3)"); pg.wait_for_timeout(500); pg.screenshot(path='/home/claude/w/shot_fr.png')
        if w==390 and lg=='ar': pg.evaluate("()=>window.__T.go('lesson','tr-l2',0)"); pg.wait_for_timeout(500); pg.screenshot(path='/home/claude/w/shot_ar.png')
        ctx.close()
    b.close()
print(json.dumps({k:v for k,v in res.items() if k!='issues'},ensure_ascii=False)); print(len(res['issues']))
for i in res['issues'][:12]: print(i)
