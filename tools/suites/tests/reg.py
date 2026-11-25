import hashlib,json,h
from h import *
def run(path):
    h.ROOT=path; out={}
    with sync_playwright() as p:
        b=p.chromium.launch()
        for lg in ['fr','en','ar']:
            ctx,pg,errs=open_page(b,1280,900)
            land=pg.evaluate("()=>document.querySelector('#app').innerHTML.length")
            out[(lg,'landing')]=land
            for ch in ['basics','derivs','branches','continuite','racine']:
                ex=pg.evaluate("(c)=>{const T=window.__T;return !!T.CH.find(x=>x.id===c)}",ch)
                if not ex: out[(lg,ch)]='absent'; continue
                pg.evaluate(INIT,[lg,ch])
                info=pg.evaluate("(c)=>{const T=window.__T;const C=T.CH.find(x=>x.id===c);return {les:(C.lessons||[]).map(l=>[l.id,(l.steps||[]).length||1]),ex:C.exercises||[]}}",ch)
                for lid,n in info['les']:
                    for st in range(n):
                        pg.evaluate("([l,s])=>window.__T.go('lesson',l,s)",[lid,st]); pg.wait_for_timeout(40)
                        out[(lg,ch,lid,st)]=hashlib.md5(pg.evaluate("()=>document.querySelector('#lw').innerHTML").encode()).hexdigest()
                pg.evaluate("()=>{const T=window.__T;T.LS.egOk=true;T.LS.phxOk=true}")
                for k in range(len(info['ex'])):
                    pg.evaluate("([i])=>{const T=window.__T;const id=T.CH.find(x=>x.id===arguments)}",[k]) if False else None
                for tier in ['ve','e','m','h','x']:
                    cnt=pg.evaluate("([t,c])=>{const T=window.__T;return (T.CH.find(x=>x.id===c).exercises||[]).filter(i=>T.EXB[i]&&T.EXB[i].d===t).length}",[tier,ch])
                    for i in range(cnt):
                        pg.evaluate("([t,i])=>window.__T.go('exercises',t,i)",[tier,i]); pg.wait_for_timeout(40)
                        out[(lg,ch,'ex',tier,i)]=hashlib.md5(pg.evaluate("()=>document.querySelector('#lw').innerHTML").encode()).hexdigest()
            ctx.close()
        b.close()
    return out
a=run('/home/claude/work/test/index_base.html'); b=run('/home/claude/work/test/index_test.html')
diff=[k for k in set(a)|set(b) if a.get(k)!=b.get(k)]
print('pages compared',len(a),'identical',len(a)-len(diff),'diff',len(diff))
for k in sorted(diff,key=str)[:15]: print(k,a.get(k),b.get(k))
