from h import *
CHECK=r"""()=>{const lw=document.querySelector('#lw');const tx=lw.innerText;const o={len:tx.length};
o.kerr=lw.querySelectorAll('.katex-error').length;o.raw=lw.querySelectorAll('.lwraw').length;o.dollar=(tx.match(/\$/g)||[]).length;
o.star=(tx.match(/\*\*|(^|\s)\*[^\s*]/g)||[]).length;o.hov=document.documentElement.scrollWidth>document.documentElement.clientWidth+2;
o.nk=lw.querySelectorAll('.katex').length;o.markers=/\[R\d+\]/.test(tx);o.notes=/Notes de restauration|Source corrompue|Corrupted source|restoration/i.test(tx);return o}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,hh in [(1280,900),(390,844)]:
        for lg in ['fr','en','ar']:
            ctx,pg,errs=open_page(b,w,hh); pg.evaluate(INIT,[lg,'suites'])
            pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true;T.go('exercises','x',0)}"); pg.wait_for_timeout(700)
            r=pg.evaluate(CHECK)
            if pg.query_selector('#lw [data-a=view]'): pg.click('#lw [data-a=view]'); pg.wait_for_timeout(500)
            r2=pg.evaluate(CHECK)
            bad=[k for k in ('kerr','raw','dollar','star','hov','markers','notes') if r2.get(k) or r.get(k)]
            print(w,lg,'len',r['len'],'->',r2['len'],'katex',r2['nk'],'issues',bad,[e for e in errs if 'createClient' not in e])
            if (w,lg)==(1280,'fr'): pg.screenshot(path='phx.png')
            ctx.close()
    b.close()
