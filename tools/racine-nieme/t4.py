from t2 import *
def start(pg):
    pg.goto('file:///home/claude/p/mythos-math/index.html#/new'); pg.wait_for_timeout(800)
    pg.click('text=BAC PC/SVT'); pg.click('text=COMMENCER LA SESSION'); pg.wait_for_timeout(1500)
    pg.click('[data-v=racine]'); pg.wait_for_timeout(500)
def btns(pg): return pg.eval_on_selector_all('button[data-a]','els=>els.map(e=>e.dataset.a+":"+(e.dataset.v||"")+":"+e.innerText.slice(0,28).replace(/\\n/g," "))')
if __name__=='__main__':
  with sync_playwright() as p:
    b,pg,errs=mk(p); start(pg)
    print(pg.inner_text('.lwstep')[:500]); print(btns(pg))
    pg.click('[data-a=golesson]'); pg.wait_for_timeout(500)
    print(btns(pg)); print(pg.inner_text('.lwstep')[:400]); pg.screenshot(path='/tmp/l1.png'); print(errs); b.close()
