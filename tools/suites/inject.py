import re,shutil,os
P='/home/claude/p/mythos-math/'
src=P+'backup/index.before-suites.html'
s=open(src,encoding='utf-8').read()
blk=open('/home/claude/p/su_block.js',encoding='utf-8').read()
# 1) data block after the Racine CH.push
m=re.search(r"CH\.push\(\{id:'racine'.*?tracks:\['PC','SM','SVT'\]\}\);\n",s,re.S); assert m
s=s[:m.end()]+blk.lstrip('\n')+s[m.end():]
# 2) chapter-picker button (next to Racine's)
old=("${CH.filter(c=>c.id==='racine'&&c.tracks.includes(LS.track)).map(c=>`<button type=\"button\" class=\"lwb lwcard\" data-a=\"go-c\" data-v=\"racine\"><b>${esc(TI(c.title))}</b><br><small>${t('rnD')}</small></button>`).join('')}")
assert s.count(old)==1
s=s.replace(old,old+old.replace("'racine'","'suites'").replace('"racine"','"suites"').replace("t('rnD')","t('suD')"))
# 3) layout class (same as Racine/Continuité)
o2="LS.chapter==='continuite'||LS.chapter==='racine'?' lwder'"
assert s.count(o2)==1
s=s.replace(o2,"LS.chapter==='continuite'||LS.chapter==='racine'||LS.chapter==='suites'?' lwder'")
# 4) lesson body spacing class (same spacing as Racine lessons)
o3="${les.id.indexOf('rn-')===0?' rnb':''}"
assert s.count(o3)==1
s=s.replace(o3,"${les.id.indexOf('rn-')===0||les.id.indexOf('su-')===0?' rnb':''}")
# 5) CSS scoped to Suites (apps/exercises spacing as Racine + domino figure, light/dark)
css=('.lwa[data-k^="su-"] .lws p,.lwa[data-k^="ex:su-"] .lws p{margin:16px 0 4px}.lwa[data-k^="su-"] .lwm,.lwa[data-k^="ex:su-"] .lwm{padding:10px 0;margin:6px 0}'
 '.lwa[data-k^="su-"] .lwm .katex-display,.lwa[data-k^="ex:su-"] .lwm .katex-display{margin:.7em 0}.lwa[data-k^="su-"]>p,.lwa[data-k^="ex:su-"]>p{margin:10px 0}'
 '.coimg:has(img[src*="assets/suites/"]){background:transparent;border-color:transparent;padding:6px}.coimg img[src*="assets/suites/"]{max-width:min(100%,560px);mix-blend-mode:normal;filter:none}'
 '[data-theme=dark] .coimg:has(img[src*="dominoes_black"]),[data-theme=light] .coimg:has(img[src*="dominoes_white"]){display:none}')
anchor='.lwa[data-k^="rn-"]>p,.lwa[data-k^="ex:rn-"]>p{margin:10px 0}'
assert s.count(anchor)==1
s=s.replace(anchor,anchor+css)
open(P+'index.html','w',encoding='utf-8').write(s)
os.makedirs(P+'assets/suites',exist_ok=True)
for n in ('dominoes_black.png','dominoes_white.png'): shutil.copy('/home/claude/p/'+('dom_'+n),P+'assets/suites/'+n)
print('injected',len(s))
