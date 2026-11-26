import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900)
    pg.evaluate(INIT,['fr','complexes']); pg.wait_for_timeout(300)
    pg.evaluate("()=>window.__T.go('lesson','cx-l6',4)"); pg.wait_for_timeout(700)
    print(pg.evaluate("""()=>{const t=document.querySelector('#lw').innerText;const out=[];let i=-1;while((i=t.indexOf('$',i+1))>=0)out.push(t.slice(Math.max(0,i-80),i+80));return out}"""))
    print(pg.evaluate("""()=>[...document.querySelectorAll('#lw .lwm')].slice(0,40).map(e=>{const k=e.querySelector('.katex');return [e.clientWidth,e.scrollWidth,k?Math.round(k.getBoundingClientRect().width):0,getComputedStyle(e).overflowX]}).filter(a=>a[1]>a[0]+3).slice(0,6)"""))
    pg.evaluate("()=>window.__T.go('lesson','cx-l3',0)"); pg.wait_for_timeout(500)
    print(pg.evaluate("""()=>[...document.querySelectorAll('#lw .lwm')].map(e=>{const k=e.querySelector('.katex');return [e.clientWidth,e.scrollWidth,k?Math.round(k.getBoundingClientRect().width):0,getComputedStyle(e).overflowX,e.className]}).filter(a=>a[1]>a[0]+3).slice(0,6)"""))
    b.close()
