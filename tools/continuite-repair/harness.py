import re,json,sys
from playwright.sync_api import sync_playwright
P='/home/claude/mythos-math/'
h=open(P+'index.html',encoding='utf8').read()
styles='\n'.join(re.findall(r'<style[^>]*>([\s\S]*?)</style>',h))
KD='/home/claude/.npm-global/lib/node_modules/markdownlint-cli2/node_modules/katex/dist/'
d=json.load(open('/home/claude/work/sample.json'))
def rich(s):
    return s
page=f'''<!doctype html><html lang="fr" dir="ltr" data-theme="THEME"><head><meta charset="utf-8"><base href="file://{P}">
<link rel="stylesheet" href="file://{KD}katex.min.css"><style>{styles}</style>
<script src="file://{KD}katex.min.js"></script></head><body style="background:var(--bg);color:var(--fg);padding:20px;max-width:820px;margin:auto;font-family:var(--ui)">
<div id="out"></div>
<script>
const SAMPLE={json.dumps(d,ensure_ascii=False)};
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
const KT=(s,dm)=>katex.renderToString(s,{{displayMode:!!dm,throwOnError:false,strict:false}});
function rich(s){{return String(s).split('**').map((seg,i)=>{{const h=seg.split(/\\$([^$]+)\\$/).map((p,j)=>j%2?KT(p,0):esc(p)).join('');return i%2?'<b>'+h+'</b>':h}}).join('')}}
let html='';
for(const f of SAMPLE.figs) html+=`<figure class="coimg ${{/fig1_tvi/.test(f)?'co-dk':'co-lt'}}"><img src="${{f}}"></figure>`;
for(const t of SAMPLE.texts) html+='<p>'+rich(t)+'</p>';
document.getElementById('out').innerHTML=html;
</script></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for th in ('dark','light'):
        pg=b.new_page(viewport={'width':900,'height':1000})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        open('/tmp/h_%s.html'%th,'w',encoding='utf8').write(page.replace('THEME',th))
        pg.goto('file:///tmp/h_%s.html'%th); pg.wait_for_timeout(800)
        pg.screenshot(path='/home/claude/shot_%s.png'%th,full_page=True)
        print(th,'errors',errs[:3],'scrollW',pg.evaluate('document.documentElement.scrollWidth'),pg.evaluate('innerWidth'))
    b.close()
