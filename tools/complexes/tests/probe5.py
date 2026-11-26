import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900)
    pg.evaluate(INIT,['fr','complexes']); pg.wait_for_timeout(300)
    pg.evaluate("()=>window.__T.go('lesson','cx-l6',1)"); pg.wait_for_timeout(300)
    pg.evaluate("()=>document.querySelectorAll('#lw [data-a=\"view\"]').forEach(b=>b.click())"); pg.wait_for_timeout(1500)
    print(pg.evaluate("""()=>[...document.querySelectorAll('#lw .lwm')].filter(e=>e.scrollWidth>e.clientWidth+3).map(e=>{const k=e.querySelector('.katex');return [e.clientWidth,e.scrollWidth,k.style.fontSize,getComputedStyle(k).fontSize,e.parentElement.className, !!e.closest('.lwa'), (e.closest('.lwa')||{dataset:{}}).dataset.k]})"""))
    print(pg.evaluate("""()=>{const e=[...document.querySelectorAll('#lw .lwm')].find(e=>e.scrollWidth>e.clientWidth+3);if(!e)return 'none';return [e.matches('.lwa[data-k^="cx-"] .lwm'),e.matches('.lwbody.cxb .lwm'),e.className, e.closest('.lwa')&&e.closest('.lwa').getAttribute('data-k')]}"""))
    b.close()
