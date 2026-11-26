import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900)
    pg.evaluate(INIT,['fr','complexes']); pg.wait_for_timeout(300)
    pg.evaluate("()=>window.__T.go('lesson','cx-l3',0)"); pg.wait_for_timeout(600)
    print(pg.evaluate("""()=>{const e=[...document.querySelectorAll('#lw .lwm')].find(e=>e.scrollWidth>e.clientWidth+3);if(!e)return 'none';
    const r=e.getBoundingClientRect();const out=[];e.querySelectorAll('*').forEach(c=>{const q=c.getBoundingClientRect();if(q.right>r.right+2||q.left<r.left-2)out.push([c.className,Math.round(q.left-r.left),Math.round(q.right-r.right),getComputedStyle(c).position])});
    return [e.clientWidth,e.scrollWidth,out.slice(0,6),e.querySelector('annotation').textContent.slice(0,80)]}"""))
    b.close()
