import sys; sys.path.insert(0,'/home/claude/tahahamam01/mythos-math/tools/complexes/tests')
from h import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=open_page(b,1280,900); pg.evaluate(INIT,['fr','complexes']); pg.wait_for_timeout(300)
    pg.evaluate("t=>{document.documentElement.dataset.theme=t}",'light')
    pg.evaluate("()=>window.__T.go('lesson','cx-l6',2)"); pg.wait_for_timeout(1200)
    print(pg.evaluate("""()=>{let e=[...document.querySelectorAll('#lw .coimg img')].find(i=>i.offsetParent);const out=[];while(e&&e!==document.documentElement){const c=getComputedStyle(e);const f=[];
      if(c.isolation==='isolate')f.push('isolation');if(c.opacity!=='1')f.push('opacity='+c.opacity);if(c.transform!=='none')f.push('transform');if(c.filter!=='none')f.push('filter');if(c.willChange!=='auto')f.push('will-change='+c.willChange);if(c.position==='fixed'||c.position==='sticky')f.push(c.position);if(c.mixBlendMode!=='normal')f.push('blend='+c.mixBlendMode);if(c.backdropFilter&&c.backdropFilter!=='none')f.push('backdrop');if(c.overflow!=='visible')f.push('overflow='+c.overflow);if(c.zIndex!=='auto'&&c.position!=='static')f.push('z='+c.zIndex);
      out.push((e.tagName+'.'+(e.className||'').toString().slice(0,30)+(e.id?'#'+e.id:''))+' '+f.join(','));e=e.parentElement}return out}"""))
    b.close()
