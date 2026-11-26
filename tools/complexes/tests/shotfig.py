import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
SC='/tmp/claude-0/-home-claude/1172a3da-d14e-52ac-ae2c-05145723c309/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch()
    for lg,th in (('fr','light'),('en','dark'),('ar','light')):
        ctx,pg,errs=open_page(b,1280,900); pg.evaluate(INIT,[lg,'complexes']); pg.wait_for_timeout(300)
        pg.evaluate("t=>{document.documentElement.dataset.theme=t}",th)
        pg.evaluate("()=>window.__T.go('lesson','cx-l6',4)"); pg.wait_for_timeout(900)
        pg.evaluate("t=>{document.documentElement.dataset.theme=t}",th); pg.wait_for_timeout(500)
        print(lg,th,pg.evaluate("()=>[...document.querySelectorAll('#lw .coimg img')].filter(i=>i.offsetParent).map(i=>[i.getAttribute('src'),i.naturalWidth])"))
        el=pg.query_selector('#lw .coimg:has(img[src*="pageab"])'); el.scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        pg.screenshot(path=SC+f'fig_{lg}_{th}.png'); ctx.close()
    b.close()
