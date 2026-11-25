const katex=require('/home/claude/.npm-global/lib/node_modules/markdownlint-cli2/node_modules/katex');
const fs=require('fs');
const strs=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let bad=0,n=0;
for(const s of strs){const re=/\$([^$]+)\$/g;let m;while((m=re.exec(s))){n++;try{katex.renderToString(m[1],{throwOnError:true,strict:'error'})}catch(e){bad++;console.log('BAD:',m[1],'|',e.message.slice(0,80))}}}
console.log('checked',n,'bad',bad);
