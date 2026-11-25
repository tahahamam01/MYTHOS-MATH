from playwright.sync_api import sync_playwright
import sys,json
KD='/home/claude/.npm-global/lib/node_modules/markdownlint-cli2/node_modules/katex/dist'
def mk(p,lang='fr',theme=None,w=1100):
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':w,'height':900}); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    def r(route):
        u=route.request.url
        if 'katex.min.js' in u: route.fulfill(path=KD+'/katex.min.js',content_type='application/javascript')
        elif 'katex.min.css' in u: route.fulfill(path=KD+'/katex.min.css',content_type='text/css')
        elif 'supabase-js' in u: route.fulfill(path='/home/claude/work/stub.js',content_type='application/javascript')
        elif u.startswith('file:') or u.startswith('data:'): route.continue_()
        else: route.abort()
    ctx.route('**/*',r)
    pg.goto('file:///home/claude/p/mythos-math/index.html'); pg.wait_for_timeout(1200)
    return b,pg,errs
if __name__=='__main__':
    with sync_playwright() as p:
        b,pg,errs=mk(p)
        print(errs); pg.goto('file:///home/claude/p/mythos-math/index.html#/new'); pg.wait_for_timeout(1500)
        pg.screenshot(path='/tmp/new.png'); print(pg.inner_text('body')[:600]); b.close()
