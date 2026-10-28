const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');
(async()=>{const [mode,out]=process.argv.slice(2);const words=JSON.parse(fs.readFileSync(__dirname+'/words.json'));
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/scene.html');await p.evaluate(()=>document.fonts.ready);
await p.evaluate(async()=>{await Promise.all(['800 40px Manrope','500 40px Manrope','40px Anton'].map(f=>document.fonts.load(f)))});
const END=await p.evaluate(w=>setup(w),words);
const dec=d=>Buffer.from(d.split(',')[1],'base64');
if(mode==='stills'){const ts=(process.env.TS||'1.5,3.6,5.3,10.5,16.8,18.9,21.8,23.9,26.2').split(',').map(Number);for(const t of ts){fs.writeFileSync(`${out}/s_${t}.jpg`,dec(await p.evaluate(t=>render(t),t)));}}
else{const fps=30,dur=Math.round(END*30)/30,n=Math.round(fps*dur);const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',''+fps,'-i','-','-i',__dirname+'/voice.mp3','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-af','apad','-t',''+dur,'-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
for(let i=0;i<n;i++){const d=await p.evaluate(t=>render(t),i/fps);if(!ff.stdin.write(dec(d)))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();await new Promise(r=>ff.on('close',r));}
await b.close();})();
