import sys
sys.path.insert(0,'/home/claude/work/proj/mythos-math/tools/racine-nieme')
from t4 import *
def shot(lang,tier,idx,name):
  with sync_playwright() as p:
    b,pg,errs=mk(p,w=900); start(pg)
    if lang!='fr': pg.click('button[data-l=%s]'%lang); pg.wait_for_timeout(300)
    pg.click('button[data-a=go-ex] >> nth=0'); pg.wait_for_timeout(200)
    pg.click('button[data-a=extier][data-v=%s]'%tier); pg.wait_for_timeout(250)
    if pg.locator('.phxw button.lwb.pri').count(): pg.click('.phxw button.lwb.pri'); pg.wait_for_timeout(250)
    pg.click('button[data-a=exnav][data-v="%d"]'%(idx-1)); pg.wait_for_timeout(150)
    if pg.locator('button[data-a=view]').count(): pg.click('button[data-a=view]'); pg.wait_for_timeout(300)
    pg.locator('.lwa').first.screenshot(path='/tmp/%s.png'%name); b.close()
shot('ar','h',5,'ar_eagle05')
shot('ar','h',12,'ar_eagle12')
shot('fr','x',1,'fr_phx01')
shot('en','ve',6,'en_chick06')
