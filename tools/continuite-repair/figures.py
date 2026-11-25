# imgHTML: add source-tone class; CSS: themed plate
old_img="return `<figure class=\"coimg\"><img src="
assert old_img in new
new=new.replace(old_img,"return `<figure class=\"coimg ${/fig1_tvi/.test(g.src)?'co-dk':'co-lt'}\"><img src=",1)
oldcss=".coimg{margin:12px 0;text-align:center}.coimg img{max-width:100%;height:auto}.coimg figcaption{font-size:.9em;opacity:.85;margin-top:6px}"
assert oldcss in new
newcss=""".coimg{margin:18px auto;padding:14px;max-width:min(100%,780px);box-sizing:border-box;text-align:center;border-radius:14px;border:1px solid var(--ln);isolation:isolate}
[data-theme=dark] .coimg{background:#151515}
[data-theme=light] .coimg{background:#c6c7c0}
.coimg img{display:block;margin:0 auto;max-width:100%;height:auto;border:0;outline:0;background:transparent}
.coimg figcaption{font-size:.9em;opacity:.85;margin-top:6px}
/* artwork is a raster with its own background: blend it into the themed plate (no white box, no blue frame) */
[data-theme=light] .coimg.co-lt img{mix-blend-mode:multiply}
[data-theme=dark] .coimg.co-lt img{filter:invert(1) hue-rotate(180deg);mix-blend-mode:screen}
[data-theme=dark] .coimg.co-dk img{mix-blend-mode:normal}
[data-theme=light] .coimg.co-dk img{filter:invert(1) hue-rotate(180deg) brightness(1.09);mix-blend-mode:multiply}
.coimg img[src*="fig3_application"]{max-width:min(100%,520px)}
.coimg img[src*="fig1_tvi"]{clip-path:inset(3px 3px 3px 0)}"""
new=new.replace(oldcss,newcss,1)
