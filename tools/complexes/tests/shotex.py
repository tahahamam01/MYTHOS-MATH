import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
SC='/tmp/claude-0/-home-claude/1172a3da-d14e-52ac-ae2c-05145723c309/scratchpad/'
lang,theme,tier,i,name=sys.argv[1:6]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900)
    pg.evaluate(INIT,[lang,'complexes']); pg.wait_for_timeout(300)
    pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
    pg.evaluate("([t,i])=>window.__T.go('exercises',t,i)",[tier,int(i)]); pg.wait_for_timeout(700)
    pg.evaluate("()=>document.querySelectorAll('#lw [data-a=\"view\"],#lw [data-a=\"showc\"]').forEach(b=>b.click())"); pg.wait_for_timeout(800)
    pg.evaluate("t=>{document.documentElement.dataset.theme=t}",theme); pg.wait_for_timeout(700)
    pg.screenshot(path=SC+name+'.png',full_page=True); print(errs[:2]); b.close()
