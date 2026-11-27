import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
from PIL import Image
SC='/tmp/claude-0/-home-claude/1172a3da-d14e-52ac-ae2c-05145723c309/scratchpad/'
# (lesson, step index) holding each figure type
T=[('cx-l2',1,'ensembles'),('cx-l6',0,'plan'),('cx-l6',2,'line'),('cx-l6',4,'pageab')]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900); pg.evaluate(INIT,['fr','complexes']); pg.wait_for_timeout(300)
    pg.evaluate("t=>{document.documentElement.dataset.theme=t}",'light')
    shots=[]
    for les,st,name in T:
        pg.evaluate("([l,s])=>window.__T.go('lesson',l,s)",[les,st]); pg.wait_for_timeout(900)
        pg.evaluate("t=>{document.documentElement.dataset.theme=t}",'light'); pg.wait_for_timeout(500)
        el=pg.query_selector('#lw .coimg:has(img[src*="complexes"])')
        if not el: print('no fig',name); continue
        el.scroll_into_view_if_needed(); pg.wait_for_timeout(400)
        f=SC+f'light_{name}.png'; el.screenshot(path=f); shots.append(f)
        im=pg.evaluate("()=>{const i=[...document.querySelectorAll('#lw .coimg img')].find(i=>i.offsetParent);const c=getComputedStyle(i);return [i.getAttribute('src'),c.mixBlendMode,c.borderRadius]}"); print(name,im)
    b.close()
ims=[Image.open(f).convert('RGB') for f in shots]
for i in ims: i.thumbnail((640,520))
W=sum(i.width for i in ims[:2])+20; sheet=Image.new('RGB',(1300,1100),(211,212,205)); x=y=0
for k,i in enumerate(ims): sheet.paste(i,((k%2)*650,(k//2)*540))
sheet.save(SC+'light_all.png')
