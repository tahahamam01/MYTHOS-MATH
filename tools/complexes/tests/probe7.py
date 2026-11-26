import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900); pg.evaluate(INIT,['fr','complexes']); pg.wait_for_timeout(300)
    pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
    pg.evaluate("()=>window.__T.go('exercises','h',8)"); pg.wait_for_timeout(400)
    pg.evaluate("()=>document.querySelectorAll('#lw [data-a=\"view\"],#lw [data-a=\"showc\"]').forEach(b=>b.click())"); pg.wait_for_timeout(1500)
    print(pg.evaluate("""()=>[...document.querySelectorAll('#lw .lwm')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>{const k=e.querySelector('.katex');const d=e.querySelector('.katex-display');return [e.clientWidth,e.scrollWidth,k.style.fontSize,getComputedStyle(k).fontSize,k.getBoundingClientRect().width,e.firstElementChild.className,[...e.children].length, getComputedStyle(e).paddingLeft]})"""))
    b.close()
