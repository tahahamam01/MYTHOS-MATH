import sys,re,difflib,os; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
import h
from h import *
def get(root):
    h.ROOT=root
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900)
        pg.evaluate(INIT,['fr','basics']); pg.wait_for_timeout(200)
        pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
        pg.evaluate("()=>window.__T.go('exercises','ve',0)"); pg.wait_for_timeout(300)
        t=pg.evaluate("()=>document.querySelector('#lw').innerText"); ids=pg.evaluate("()=>[...Object.keys(window.__T.EXB)].length")
        b.close(); return t,ids
a,ia=get('/home/claude/work/test/index_base.html'); b,ib=get('/home/claude/work/test/index_test.html')
print(ia,ib); print('--- base:\n',a[:300].replace('\n',' | ')); print('--- new:\n',b[:300].replace('\n',' | '))
import difflib
for l in difflib.unified_diff(a.split('\n'),b.split('\n'),lineterm='',n=0): print(l[:200])
