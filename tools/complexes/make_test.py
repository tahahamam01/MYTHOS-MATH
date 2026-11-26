"""Build a test copy of index.html that exposes internals as window.__T (the app is one IIFE)."""
import sys
src=sys.argv[1]; dst=sys.argv[2]
s=open(src,encoding='utf-8').read()
hook=("window.__T=Object.defineProperties({},{"
 "guard:{get:()=>guard,set:v=>{guard=v}},lang:{get:()=>lang,set:v=>{lang=v}},sess:{get:()=>sess,set:v=>{sess=v}},"
 "LS:{get:()=>LS,set:v=>{LS=v}},newLS:{get:()=>newLS},render:{get:()=>render},go:{get:()=>go},CH:{get:()=>CH},EXB:{get:()=>EXB},APPBANK:{get:()=>APPBANK}});\n")
k="render();size();if(!RM)raf=requestAnimationFrame(frame);\naddEventListener('DOMContentLoaded',initAuth);\n})();"
assert s.count(k)==1
open(dst,'w',encoding='utf-8').write(s.replace(k,hook+k))
print('ok')
