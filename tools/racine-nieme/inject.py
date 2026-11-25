import re,shutil
P='/home/claude/p/mythos-math/'
shutil.copy(P+'backup/index.before-racine-nieme.html',P+'index.html')
s=open(P+'index.html',encoding='utf8').read()
blk=open('/home/claude/work/rn_block.js',encoding='utf8').read()
m=re.search(r"CH\.push\(\{id:'continuite'.*?tracks:\['PC','SVT'\]\}\);\n",s,re.S)
assert m
s=s[:m.end()]+blk.lstrip('\n')+s[m.end():]
old="${CH.filter(c=>c.id==='continuite'&&c.tracks.includes(LS.track)).map(c=>`<button type=\"button\" class=\"lwb lwcard\" data-a=\"go-c\" data-v=\"continuite\"><b>${esc(TI(c.title))}</b><br><small>${t('coD')}</small></button>`).join('')}"
assert s.count(old)==1
s=s.replace(old,old+old.replace("'continuite'","'racine'").replace('"continuite"','"racine"').replace("t('coD')","t('rnD')"))
o2="LS.chapter==='continuite'?' lwder'"
assert s.count(o2)==1
s=s.replace(o2,"LS.chapter==='continuite'||LS.chapter==='racine'?' lwder'")
open(P+'index.html','w',encoding='utf8').write(s)
print('injected',len(s))
