from playwright.sync_api import sync_playwright
KD='/home/claude/.npm-global/lib/node_modules/markdownlint-cli2/node_modules/katex/dist/'
stub="window.supabase={createClient:()=>({auth:{getSession:async()=>({data:{session:null}}),onAuthStateChange:()=>({data:{subscription:{unsubscribe(){}}}}),signInWithPassword:async()=>({}),signOut:async()=>({})},from:()=>({select:()=>({eq:()=>({order:async()=>({data:[]})})})})})};"
def route(r):
    u=r.request.url
    if 'katex.min.js' in u: r.fulfill(path=KD+'katex.min.js',content_type='application/javascript')
    elif 'katex.min.css' in u: r.fulfill(path=KD+'katex.min.css',content_type='text/css')
    elif 'supabase-js' in u: r.fulfill(body=stub,content_type='application/javascript')
    elif u.startswith('file://'): r.continue_()
    else: r.abort()
with sync_playwright() as p:
    b=p.chromium.launch()
    for th in('dark','light'):
      for lang in ('fr','en','ar'):
        pg=b.new_page(viewport={'width':1100,'height':800}); errs=[]
        pg.on('pageerror',lambda e:errs.append('PAGEERR '+str(e)[:150])); pg.on('console',lambda m: errs.append(m.text[:150]) if m.type=='error' else None)
        pg.route('**/*',route)
        pg.goto('file:///home/claude/mythos-math/index.html'); pg.wait_for_timeout(800)
        pg.evaluate(f"document.documentElement.setAttribute('data-theme','{th}');document.documentElement.lang='{lang}'")
        pg.wait_for_timeout(300)
        print(th,lang,'errors:',[e for e in errs if 'ERR_FAILED' not in e][:4],'scrollW',pg.evaluate('document.documentElement.scrollWidth'),'/',pg.evaluate('innerWidth'))
        if th=='dark' and lang=='fr': pg.screenshot(path='/home/claude/landing.png')
    b.close()
