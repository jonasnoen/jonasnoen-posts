// Usage: node shot.cjs <slides.html> <outdir>   -> ig-01..NN.png (1080x1350) + tt-01..NN.png (1080x1920)
// Vorlage v2 (Slides mit <div class="in">): TikTok-Version per body.tt. Alte Vorlage (K001 v1): Stil-Patch.
const {chromium}=require('playwright');const path=require('path');
(async()=>{const src=path.resolve(process.argv[2]||__dirname+'/slides.html');const out=path.resolve(process.argv[3]||__dirname);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:2000}});
await p.goto('file://'+src);await p.evaluate(async()=>{await document.fonts.ready;await Promise.all(['800 40px Manrope','500 40px Manrope','40px Anton','italic 40px Serif'].map(f=>document.fonts.load(f)))});
await p.waitForTimeout(300);const n=await p.locator('section.slide').count();const nn=i=>String(i).padStart(2,'0');
for(let i=1;i<=n;i++)await p.locator('#s'+i).screenshot({path:`${out}/ig-${nn(i)}.png`});
const v2=await p.evaluate(()=>!!document.querySelector('.slide .in'));
if(v2)await p.evaluate(()=>document.body.classList.add('tt'));
else await p.addStyleTag({content:'.slide{height:1920px!important}.pad,.lamp,.cone,.stamp,canvas.guy{transform:translateY(240px)}.stack{bottom:360px!important}.stack-l{bottom:530px!important}.foot{bottom:300px!important}'});
await p.waitForTimeout(200);
for(let i=1;i<=n;i++)await p.locator('#s'+i).screenshot({path:`${out}/tt-${nn(i)}.png`});
await b.close();})();
