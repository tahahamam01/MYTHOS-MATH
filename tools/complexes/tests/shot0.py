import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
SC='/tmp/claude-0/-home-claude/1172a3da-d14e-52ac-ae2c-05145723c309/scratchpad/'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900)
    print(pg.evaluate(INIT,['fr','suites'])); pg.wait_for_timeout(500)
    pg.screenshot(path=SC+'su_chap.png')
    pg.evaluate("()=>window.__T.go('lesson','su-l2',1)"); pg.wait_for_timeout(600)
    pg.screenshot(path=SC+'su_lesson.png',full_page=False)
    print(errs[:3]); b.close()
