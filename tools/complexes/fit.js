(()=>{let t=0;const SEL='.lwbody.cxb .lwm,.lwa[data-k^="cx-"] .lwm,.lwa[data-k^="ex:cx-"] .lwm';
const fit=()=>{t=0;document.querySelectorAll(SEL).forEach(e=>{const k=e.querySelector('.katex');if(!k)return;k.style.removeProperty('font-size');const FL=innerWidth>700?0.5:0.62;const f0=parseFloat(getComputedStyle(k).fontSize);let f=f0;for(let i=0;i<4;i++){const cw=e.clientWidth,sw=e.scrollWidth;if(!(cw>0&&sw>cw+1))break;f=Math.max(f*cw/sw*0.96,f0*FL);k.style.setProperty('font-size',f+'px','important');if(f<=f0*FL+0.01)break}})};
const q=()=>{if(!t)t=requestAnimationFrame(fit);setTimeout(fit,400)};
new MutationObserver(q).observe(document.body,{childList:true,subtree:true});addEventListener('resize',q);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(q)})();
