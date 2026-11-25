from t4 import *
JS="""()=>{const out=[];document.querySelectorAll('.lwstep p, .lwstep li, .lwstep td, .lwstep th, .lwstep h2, .lwstep h3').forEach(e=>{const c=e.cloneNode(true);c.querySelectorAll('.katex').forEach(k=>k.remove());const t=c.innerText.trim();if(/[A-Za-z]{4,}/.test(t)&&!/[\\u0600-\\u06FF]/.test(t))out.push(t.slice(0,80))});return out}"""
with sync_playwright() as p:
    b,pg,errs=mk(p); start(pg); pg.click('button[data-l=ar]'); pg.wait_for_timeout(400)
    print(pg.evaluate("document.documentElement.dir"), pg.inner_text('.lwstep')[:100].replace('\n',' '))
    bad=[]
    for L in ['rn-l1','rn-l2','rn-l3','rn-l4','rn-l5','rn-l6']:
        pg.click('button[data-a=golesson][data-v=%s]'%L); pg.wait_for_timeout(200)
        k=pg.eval_on_selector_all('.lwnav button[data-a=gostep]','e=>e.length')
        for si in range(k):
            pg.click('.lwnav button[data-a=gostep] >> nth=%d'%si); pg.wait_for_timeout(150); bad+=pg.evaluate(JS)
            if L=='rn-l2': pg.screenshot(path='/tmp/ar_l2.png',full_page=True)
    print('untranslated AR fragments:',bad)
    # light theme shot of lesson 3 FR
    pg.click('button[data-l=fr]'); pg.wait_for_timeout(300)
    pg.click('button[data-a=golesson][data-v=rn-l5]'); pg.wait_for_timeout(300); pg.screenshot(path='/tmp/fr_l5.png')
    print(errs); b.close()
