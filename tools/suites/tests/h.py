import sys, json, pathlib
from playwright.sync_api import sync_playwright
ROOT='/home/claude/work/test/index_test.html'
KD='/opt/npm-tools/node_modules/katex/dist/'
def route(r):
    u=r.request.url
    if 'katex.min.js' in u: return r.fulfill(path=KD+'katex.min.js',content_type='application/javascript')
    if 'katex.min.css' in u:
        css=open(KD+'katex.min.css').read().replace('url(fonts/','url(https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/fonts/')
        return r.fulfill(body=css,content_type='text/css')
    if 'katex' in u and '/fonts/' in u:
        f=KD+'fonts/'+u.split('/fonts/')[1]
        if pathlib.Path(f).exists(): return r.fulfill(path=f)
    if u.startswith('file://'): return r.continue_()
    return r.abort()
def open_page(b,w=1280,h=900,theme=None):
    ctx=b.new_context(viewport={'width':w,'height':h}); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*',route); pg.goto('file://'+ROOT); pg.wait_for_timeout(1500)
    return ctx,pg,errs
INIT="""([l,ch])=>{const T=window.__T;T.guard=()=>'ok';T.lang=l;T.sess={user:{id:'t'}};T.LS=T.newLS('t','local','PC',ch);T.LS.view='chap';location.hash='#/learn';T.render();return document.querySelector('#lw')?1:0}"""
if __name__=='__main__':
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx,pg,errs=open_page(b)
        print(pg.evaluate(INIT,['fr','suites'])); pg.wait_for_timeout(800)
        print(errs, pg.evaluate("typeof katex"), pg.evaluate("document.querySelector('#lw')&&document.querySelector('#lw').innerText.slice(0,300)"))
        pg.screenshot(path='chap.png'); b.close()
