import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (1280,390):
        ctx,pg,errs=open_page(b,w,900); pg.evaluate(INIT,['fr','complexes']); pg.wait_for_timeout(300)
        pg.evaluate("()=>window.__T.go('lesson','cx-l3',0)"); pg.wait_for_timeout(1500)
        print(w,pg.evaluate("""()=>[...document.querySelectorAll('#lw .lwm')].map(e=>{const k=e.querySelector('.katex');return [e.clientWidth,e.scrollWidth,k.style.fontSize,getComputedStyle(k).fontSize,getComputedStyle(e).overflowX]})"""))
        ctx.close()
    b.close()
