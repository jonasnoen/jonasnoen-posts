// Usage: node shot.cjs <slides.html> <outdir>   -> ig-01..07.png (1080x1350) + tt-01..07.png (1080x1920)
const {chromium}=require('playwright');const path=require('path');
(async()=>{const src=path.resolve(process.argv[2]||__dirname+'/slides.html');const out=path.resolve(process.argv[3]||__dirname);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:2000}});
await p.goto('file://'+src);await p.evaluate(async()=>{await document.fonts.ready;await Promise.all(['800 40px Manrope','500 40px Manrope','40px Anton'].map(f=>document.fonts.load(f)))});
await p.waitForTimeout(300);const n=await p.locator('section.slide').count();
for(let i=1;i<=n;i++)await p.locator('#s'+i).screenshot({path:`${out}/ig-0${i}.png`});
await p.addStyleTag({content:'.slide{height:1920px!important}.pad,.lamp,.cone,.stamp,canvas.guy{transform:translateY(240px)}.stack{bottom:360px!important}.stack-l{bottom:530px!important}.foot{bottom:300px!important}'});await p.waitForTimeout(200);
for(let i=1;i<=n;i++)await p.locator('#s'+i).screenshot({path:`${out}/tt-0${i}.png`});
await b.close();})();
