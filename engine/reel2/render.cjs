// Reel-Renderer, Stil "reel2" (Text oben, KI-Avatar unten rechts, Sounds + Musik).
// Aufruf im Arbeitsordner (scene.html, words.json, voice.mp3, node_modules mit Schriften):
//   NODE_PATH=/opt/npm-tools/node_modules ASSETS=<repo>/assets node render.cjs stills <dir>     (Kontrollbilder, Zeiten über TS=1,4.5,...)
//   NODE_PATH=/opt/npm-tools/node_modules ASSETS=<repo>/assets node render.cjs full final.mp4  (fertiges Reel inkl. Ton)
// Optional: MUSIC=<datei in assets/music> (sonst wird abwechselnd nach Reel-Nummer REEL=R003 gewählt), MUSIC_VOL=0.10
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {spawn,execFileSync}=require('child_process');
const A=process.env.ASSETS||path.join(__dirname,'..','..','assets');
const run=(args)=>new Promise((res,rej)=>{const p=spawn('ffmpeg',args,{stdio:['ignore','inherit','inherit']});p.on('close',c=>c?rej(new Error('ffmpeg '+c)):res());});
(async()=>{const [mode,out]=process.argv.slice(2);const dir=process.cwd();const words=JSON.parse(fs.readFileSync(dir+'/words.json'));
  // Avatar-Posen als data-URIs (file://-Bilder würden das Canvas "verschmutzen")
  const av={};for(const f of fs.readdirSync(A+'/avatar')){if(f.endsWith('.png')&&f!=='reference.png')av[f.replace('.png','')]='data:image/png;base64,'+fs.readFileSync(A+'/avatar/'+f).toString('base64');}
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.addInitScript(d=>{window.AVDATA=d;},av);
  await p.goto('file://'+dir+'/scene.html');await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(async()=>{await Promise.all(['800 40px Manrope','500 40px Manrope','40px Anton'].map(f=>document.fonts.load(f)))});
  const END=await p.evaluate(w=>setup(w),words);await p.waitForFunction(()=>window.IMGS_READY===true,null,{timeout:30000});
  const dec=d=>Buffer.from(d.split(',')[1],'base64');
  if(mode==='stills'){const ts=(process.env.TS||'0.1,1.5,3.6,5.3,8.9,10.5,12.6,15,17.8').split(',').map(Number);for(const t of ts){fs.writeFileSync(`${out}/s_${t}.jpg`,dec(await p.evaluate(t=>render(t),t)));}await b.close();return;}
  const cues=await p.evaluate(()=>window.CUES||[]);
  const fps=30,dur=Math.round(END*30)/30,n=Math.round(fps*dur);const vid=dir+'/_video.mp4';
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',''+fps,'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',vid],{stdio:['pipe','inherit','inherit']});
  for(let i=0;i<n;i++){const d=await p.evaluate(t=>render(t),i/fps);if(!ff.stdin.write(dec(d)))await new Promise(r=>ff.stdin.once('drain',r));}
  ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();
  // ---- Ton: Stimme + leise Musik (Loop, Ein-/Ausblenden) + Effekte an den Cues ----
  const tracks=fs.readdirSync(A+'/music').filter(f=>f.endsWith('.mp3')).sort();
  const num=parseInt((process.env.REEL||'').replace(/\D/g,''))||0;const music=process.env.MUSIC||tracks[num%tracks.length];
  const mvol=process.env.MUSIC_VOL||'0.10';
  const inputs=['-i',vid,'-i',dir+'/voice.mp3','-stream_loop','-1','-i',A+'/music/'+music];
  const used=[...new Set(cues.map(c=>c.name))].filter(nm=>fs.existsSync(`${A}/sfx/${nm}.mp3`));
  used.forEach(nm=>inputs.push('-i',`${A}/sfx/${nm}.mp3`));
  let fc=`[1:a]aresample=48000,apad[v];[2:a]aresample=48000,volume=${mvol},afade=t=in:d=0.3,afade=t=out:st=${(dur-1.2).toFixed(2)}:d=1.2[m];`;
  const labels=['[v]','[m]'];
  used.forEach((nm,i)=>{const list=cues.filter(c=>c.name===nm);fc+=`[${3+i}:a]aresample=48000,asplit=${list.length}${list.map((_,j)=>`[s${i}_${j}]`).join('')};`;
    list.forEach((c,j)=>{fc+=`[s${i}_${j}]volume=${(0.55*c.vol).toFixed(2)},adelay=${Math.round(c.t*1000)}|${Math.round(c.t*1000)}[c${i}_${j}];`;labels.push(`[c${i}_${j}]`);});});
  fc+=`${labels.join('')}amix=inputs=${labels.length}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]`;
  await run(['-y','-v','error',...inputs,'-filter_complex',fc,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',''+dur,'-movflags','+faststart',out]);
  fs.unlinkSync(vid);console.log('fertig',out,'Musik:',music,'Cues:',cues.length);
})();
