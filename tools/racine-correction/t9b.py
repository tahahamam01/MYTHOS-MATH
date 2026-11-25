import sys,re,json
sys.path.insert(0,'/home/claude/work/proj/mythos-math/tools/racine-nieme')
from t4 import *
from t5 import CHK
EXP={'ve':10,'e':10,'m':11,'h':12,'x':3}
DUMP={}
def run(lang):
  with sync_playwright() as p:
    b,pg,errs=mk(p); start(pg)
    if lang!='fr': pg.click('button[data-l=%s]'%lang); pg.wait_for_timeout(300)
    n=0;kat=0;bad=0;leaks=0;rtl_bad=0
    for tier in ['ve','e','m','h','x']:
        pg.click('button[data-a=go-ex] >> nth=0'); pg.wait_for_timeout(200)
        pg.click('button[data-a=extier][data-v=%s]'%tier); pg.wait_for_timeout(250)
        if pg.locator('.phxw button.lwb.pri').count():
            print(lang,tier,'phoenix warning shown'); pg.click('.phxw button.lwb.pri'); pg.wait_for_timeout(250)
        cnt=pg.locator('.exchip').count()
        assert cnt==EXP[tier],(lang,tier,cnt)
        for i in range(cnt):
            pg.click('button[data-a=exnav][data-v="%d"]'%i); pg.wait_for_timeout(100)
            if pg.locator('button[data-a=view]').count(): pg.click('button[data-a=view]'); pg.wait_for_timeout(120)
            r=pg.evaluate(CHK); n+=1; kat+=r['kat']
            if r['err'] or r['dollar'] or r['bs'] or r['stars']: bad+=1; print('PROBLEM',lang,tier,i+1,r)
            t=pg.evaluate("""()=>{const r=document.querySelector('.lwstep');const c=r.cloneNode(true);c.querySelectorAll('.katex').forEach(k=>k.remove());return c.innerText}""")
            DUMP['%s|%s|%d'%(lang,tier,i+1)]=t
            if lang=='ar':
                if re.search(r'\b(Solve|Compute|Simplify|Show that|Compare|Since|Check|Set|Let|Form)\b',t): leaks+=1; print('EN LEAK',tier,i+1)
                if re.search(r'[A-Za-zÀ-ÿ]{4,}',re.sub(r'(Chick|Chicken|Raven|Eagle|Phoenix|CHICK|CHICKEN|RAVEN|EAGLE|PHOENIX)','',t)): print('LATIN TEXT in AR',tier,i+1,re.findall(r'[A-Za-zÀ-ÿ’]{4,}',t)[:6])
            if lang=='en' and re.search(r'\b(Calculer|Simplifier|Résoudre|Comparer|donc|Comme|Vérification|Montrer|Soit)\b',t): print('FR LEAK',tier,i+1)
        if lang=='ar':
            d=pg.evaluate("document.querySelector('.lwstep').closest('[dir]')?.getAttribute('dir')||document.documentElement.dir")
    print(lang,'checked',n,'katex nodes',kat,'problems',bad,'leaks',leaks,'jserrs',errs); b.close()
for l in ['fr','en','ar']: run(l)
json.dump(DUMP,open('/home/claude/work/dump_app.json','w',encoding='utf8'),ensure_ascii=False,indent=0)
