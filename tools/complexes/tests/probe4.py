import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
SC='/tmp/claude-0/-home-claude/1172a3da-d14e-52ac-ae2c-05145723c309/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900)
    pg.evaluate(INIT,['fr','complexes']); pg.wait_for_timeout(300)
    pg.evaluate("()=>window.__T.go('lesson','cx-l3',0)"); pg.wait_for_timeout(900)
    print(pg.evaluate("""()=>[...document.querySelectorAll('#lw .lwm')].map(e=>[e.clientWidth,e.scrollWidth,getComputedStyle(e.querySelector('.katex')).fontSize])"""))
    pg.screenshot(path=SC+'wide_fit.png',full_page=True); b.close()
