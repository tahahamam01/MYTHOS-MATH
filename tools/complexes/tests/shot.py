import sys,json; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
SC='/tmp/claude-0/-home-claude/1172a3da-d14e-52ac-ae2c-05145723c309/scratchpad/'
# usage: shot.py lang theme lesson step name [w] | ex tier idx
a=sys.argv[1:]
lang,theme,kind=a[0],a[1],a[2]
with sync_playwright() as p:
    b=p.chromium.launch(); w=int(a[6]) if len(a)>6 else 1280
    ctx,pg,errs=open_page(b,w,900)
    pg.evaluate(INIT,[lang,'complexes']); pg.wait_for_timeout(300)
    pg.evaluate("t=>{document.documentElement.dataset.theme=t}",theme)
    if kind=='chap': pass
    elif kind=='lesson': pg.evaluate("([l,s])=>window.__T.go('lesson',l,s)",[a[3],int(a[4])])
    else:
        pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
        pg.evaluate("([t,i])=>window.__T.go('exercises',t,i)",[a[3],int(a[4])])
    pg.wait_for_timeout(900)
    pg.evaluate("t=>{document.documentElement.dataset.theme=t}",theme); pg.wait_for_timeout(300)
    pg.screenshot(path=SC+a[5]+'.png',full_page=(len(a)>7))
    print([e for e in errs if 'createClient' not in e][:3]); b.close()
