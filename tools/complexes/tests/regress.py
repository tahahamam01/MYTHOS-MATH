import sys,json,hashlib,os; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
import h
from h import *
out={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for lg in ('fr','en','ar'):
        ctx,pg,errs=open_page(b,1280,900)
        ids=pg.evaluate("()=>window.__T.CH.map(c=>c.id).filter(i=>i!=='complexes')")
        for ch in ids:
            pg.evaluate(INIT,[lg,ch]); pg.wait_for_timeout(120)
            info=pg.evaluate("(ch)=>{const c=window.__T.CH.find(x=>x.id===ch);return {k:c.kind,les:(c.lessons||[]).map(l=>[l.id,l.steps.length]),ex:(c.exercises||[]).slice(0,3)}}",ch)
            for lid,n in info['les']:
                for st in range(min(n,3)):
                    pg.evaluate("([l,s])=>window.__T.go('lesson',l,s)",[lid,st]); pg.wait_for_timeout(60)
                    out[f'{lg}|{ch}|{lid}|{st}']=hashlib.md5(pg.evaluate("()=>{const e=document.querySelector('#lw');return e?e.innerHTML:''}").encode()).hexdigest()
            pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
            for tier in ('ve','e','m','h'):
                pg.evaluate("([t,i])=>{try{window.__T.go('exercises',t,i)}catch(e){document.querySelector('#lw')&&(document.querySelector('#lw').innerHTML='ERR')}}",[tier,0]); pg.wait_for_timeout(60)
                out[f'{lg}|{ch}|ex|{tier}']=hashlib.md5(pg.evaluate("()=>{const e=document.querySelector('#lw');return e?e.innerHTML:''}").encode()).hexdigest()
        ctx.close()
    b.close()
json.dump(out,open(sys.argv[1],'w')); print(len(out),'pages hashed')
