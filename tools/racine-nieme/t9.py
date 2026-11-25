import re
from t4 import *
from t5 import CHK
import sys
def run(lang):
  with sync_playwright() as p:
    b,pg,errs=mk(p); start(pg)
    if lang!='fr': pg.click('button[data-l=%s]'%lang); pg.wait_for_timeout(300)
    n=0;kat=0;bad=0;untr=0
    for tier in ['ve','e','m','h','x']:
        pg.click('button[data-a=go-ex] >> nth=0'); pg.wait_for_timeout(200)
        pg.click('button[data-a=extier][data-v=%s]'%tier); pg.wait_for_timeout(250)
        if pg.locator('.phxw button.lwb.pri').count(): pg.click('.phxw button.lwb.pri'); pg.wait_for_timeout(250)
        for i in range(9):
            pg.click('button[data-a=exnav][data-v="%d"]'%i); pg.wait_for_timeout(120)
            if pg.locator('button[data-a=view]').count(): pg.click('button[data-a=view]'); pg.wait_for_timeout(120)
            r=pg.evaluate(CHK); n+=1; kat+=r['kat']
            if r['err'] or r['dollar'] or r['bs'] or r['stars']: bad+=1; print('PROBLEM',lang,tier,i,r)
            if lang=='ar':
                t=pg.evaluate("""()=>{const r=document.querySelector('.lwstep');const c=r.cloneNode(true);c.querySelectorAll('.katex').forEach(k=>k.remove());return c.innerText}""")
                if re.search(r'\b(Solve|Compute|Simplify|Show that|Limits|Compare)\b',t): untr+=1; print('EN LEAK',tier,i)
    print(lang,'exercises checked',n,'katex',kat,'problems',bad,'leaks',untr,'jserrs',errs); b.close()
for l in ['fr','en','ar']: run(l)
