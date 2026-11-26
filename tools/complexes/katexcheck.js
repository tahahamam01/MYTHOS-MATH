// Renders every TeX string of the chapter with KaTeX (throwOnError) and reports failures.
const katex=require('/opt/npm-tools/node_modules/katex');
const fs=require('fs');
const f=process.argv[2];
const items=JSON.parse(fs.readFileSync(f,'utf8'));
let bad=0;
for(const [where,tex] of items){
  try{katex.renderToString(tex,{displayMode:true,throwOnError:true,strict:false,macros:{'\\arraystretch':'1.45'}})}
  catch(e){bad++; if(bad<=25)console.log(where,'|',tex.slice(0,90).replace(/\n/g,' '),'|',e.message.slice(0,120))}
}
console.log('checked',items.length,'failures',bad);
