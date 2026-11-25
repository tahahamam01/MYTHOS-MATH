from t4 import *
import re
CHK="""()=>{const r=document.querySelector('.lwstep')||document.body;const err=r.querySelectorAll('.katex-error,.lwraw').length;
const c=r.cloneNode(true);c.querySelectorAll('.katex').forEach(k=>k.remove());const tx=c.innerText;
return {err,kat:r.querySelectorAll('.katex').length,dollar:(tx.match(/\\$/g)||[]).length,bs:(tx.match(/\\\\[a-zA-Z]+/g)||[]),stars:(tx.match(/\\*\\*/g)||[]).length}}"""
def crawl(lang):
  with sync_playwright() as p:
    b,pg,errs=mk(p)
    start(pg)
    if lang!='fr': pg.click('button[data-l=%s]'%lang); pg.wait_for_timeout(400)
    rep=[]
    lessons=[x.split(':')[1] for x in btns(pg) if x.startswith('golesson:rn-l')]
    lessons=list(dict.fromkeys(lessons))
    for L in lessons:
        pg.click('button[data-a=golesson][data-v=%s]'%L); pg.wait_for_timeout(250)
        n=pg.eval_on_selector_all('button[data-a=gostep]','e=>e.filter(x=>x.closest(".lwnav")).length')
        steps=pg.eval_on_selector_all('.lwnav button[data-a=gostep]','e=>e.map(x=>x.dataset.s||x.dataset.v)')
        for si in range(len(steps)):
            pg.click('.lwnav button[data-a=gostep] >> nth=%d'%si); pg.wait_for_timeout(200)
            r=pg.evaluate(CHK); rep.append((L,si,r))
            if r['err'] or r['dollar'] or r['bs'] or r['stars']: print('PROBLEM',lang,L,si,r)
    print(lang,'steps checked',len(rep),'katex total',sum(r['kat'] for _,_,r in rep),'errs',errs)
    b.close()
if __name__=='__main__':
  for l in ['fr','en','ar']: crawl(l)
