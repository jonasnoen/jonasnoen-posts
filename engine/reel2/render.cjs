// Reel-Renderer, Stil "reel2" (Text oben, KI-Avatar unten rechts, Sounds + Musik).
// Aufruf im Arbeitsordner (scene.html, words.json, voice.mp3, node_modules mit Schriften):
//   NODE_PATH=/opt/npm-tools/node_modules ASSETS=<repo>/assets node render.cjs stills <dir>     (Kontrollbilder, Zeiten über TS=1,4.5,...)
//   NODE_PATH=/opt/npm-tools/node_modules ASSETS=<repo>/assets node render.cjs track base.mp4  (Avatar-Spur aus den Loops laut AVP, Greenscreen,
//      für Veed-Lipsync; Ergebnis als lipsync.mp4 in den Arbeitsordner legen)
//   NODE_PATH=/opt/npm-tools/node_modules ASSETS=<repo>/assets node render.cjs full final.mp4  (fertiges Reel inkl. Ton)
// Optional: MUSIC=<datei in assets/music> (sonst wird abwechselnd nach Reel-Nummer REEL=R003 gewählt), MUSIC_VOL=0.10
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {spawn,execFileSync}=require('child_process');
const A=process.env.ASSETS||path.join(__dirname,'..','..','assets');
const run=(args)=>new Promise((res,rej)=>{const p=spawn('ffmpeg',args,{stdio:['ignore','inherit','inherit']});p.on('close',c=>c?rej(new Error('ffmpeg '+c)):res());});
(async()=>{const [mode,out]=process.argv.slice(2);const dir=process.cwd();const words=JSON.parse(fs.readFileSync(dir+'/words.json'));
  // Avatar-Posen als data-URIs (file://-Bilder würden das Canvas "verschmutzen")
  const av={};for(const f of fs.readdirSync(A+'/avatar')){if(f.endsWith('.png')&&f!=='reference.png')av[f.replace('.png','')]='data:image/png;base64,'+fs.readFileSync(A+'/avatar/'+f).toString('base64');}
  // Lautstärke-Hüllkurve der Stimme pro Video-Frame (0..1): steuert, wie weit der Mund offen ist
  const pcm=execFileSync('ffmpeg',['-v','error','-i',dir+'/voice.mp3','-ac','1','-ar','16000','-f','s16le','-'],{maxBuffer:1<<28});
  const smp=new Int16Array(pcm.buffer,pcm.byteOffset,pcm.length>>1),hop=16000/30,env=[];
  for(let i=0;i*hop<smp.length;i++){let s=0;const a=Math.floor(i*hop),e=Math.min(smp.length,Math.floor((i+1)*hop));for(let j=a;j<e;j++)s+=smp[j]*smp[j];env.push(Math.sqrt(s/Math.max(1,e-a)));}
  const sorted=[...env].sort((x,y)=>x-y),ref=sorted[Math.floor(sorted.length*.95)]||1;
  let lv=0;const ENV=env.map(v=>{const x=Math.min(1,v/ref);lv=x>lv?lv+(x-lv)*.7:lv+(x-lv)*.35;return +lv.toFixed(3);});
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.addInitScript(([d,e])=>{window.AVDATA=d;window.ENV=e;},[av,ENV]);
  await p.goto('file://'+dir+'/scene.html');await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(async()=>{await Promise.all(['800 40px Manrope','500 40px Manrope','40px Anton',"italic 40px 'Instrument Serif'"].map(f=>document.fonts.load(f)))});
  const END=await p.evaluate(w=>setup(w),words);await p.waitForFunction(()=>window.IMGS_READY===true,null,{timeout:30000});
  const dec=d=>Buffer.from(d.split(',')[1],'base64');
  // ---- Sprech-Loops (assets/avatar/loops/<name>.mp4, Greenscreen): einmal freistellen (Cache im Arbeitsordner),
  // dann pro Frame das passende Einzelbild an die Szene geben. Pose 'loop:<name>' in AVP nutzt sie.
  const loops={};const ldir=A+'/avatar/loops';const seed=(parseInt((process.env.REEL||'').replace(/\D/g,''))||0)*97;
  if(mode==='track'){ // ---- Avatar-Spur: Loops pro Phrase aneinanderhängen, 0,3 s weich überblendet ----
    const plan=await p.evaluate(()=>window.avatarPlan());await b.close();const F=0;const segs=[]; // harter Schnitt beim Phrasenwechsel (Überblenden sah verwaschen aus)
    plan.forEach(s=>{if(segs.length&&segs[segs.length-1].loop===s.loop)return;segs.push({...s});});
    segs.forEach((s,i)=>{s.d=(i+1<segs.length?segs[i+1].t:END)-s.t;});
    const inputs=[];let fc='';segs.forEach((s,i)=>{const pp=`${dir}/_pp_${s.loop}.mp4`;
      if(!fs.existsSync(pp))execFileSync('ffmpeg',['-v','error','-y','-i',`${ldir}/${s.loop}.mp4`,'-filter_complex','[0:v]fps=30,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0[v]','-map','[v]','-an','-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',pp]);
      const len=parseFloat(execFileSync('ffprobe',['-v','error','-show_entries','format=duration','-of','csv=p=0',pp]).toString());
      const need=s.d+(i+1<segs.length?F:0),off=need<len-.1?((seed*0.37+i*3.1)%(len-need)):0;
      inputs.push('-stream_loop','-1','-ss',off.toFixed(2),'-t',need.toFixed(3),'-i',pp);fc+=`[${i}:v]fps=30,scale=1920:1080,setsar=1,format=yuv420p,settb=AVTB[s${i}];`;});
    fc+=segs.map((_,i)=>`[s${i}]`).join('')+`concat=n=${segs.length}:v=1:a=0[cat]`;const last='[cat]';
    await run(['-y','-v','error',...inputs,'-filter_complex',fc,'-map',last,'-an','-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p','-r','30','-t',END.toFixed(3),out]);
    console.log('Avatar-Spur',out,segs.map(s=>s.loop+'@'+s.t.toFixed(2)).join(' '));return;}
  const SYNC=fs.existsSync(dir+'/lipsync.mp4');if(SYNC)await p.evaluate(()=>{window.SYNC=true;});
  if(!SYNC&&fs.existsSync(ldir))for(const f of fs.readdirSync(ldir).filter(f=>f.endsWith('.mp4'))){const nm=f.replace('.mp4','');const cache=`${dir}/_loop_${nm}`;
    if(!fs.existsSync(cache+'/0000.png'))execFileSync('python3',[path.join(A,'..','engine','avatar','key_loop.py'),`${ldir}/${f}`,cache],{stdio:'inherit'});
    loops[nm]=fs.readdirSync(cache).filter(x=>x.endsWith('.png')).sort().map(x=>`${cache}/${x}`);}
  // Lippensynchrones Avatar-Video dieses Reels (lipsync.mp4 im Arbeitsordner, Greenscreen, startet bei t=0):
  // Pose 'loop:sync' zeigt exakt den Frame zur aktuellen Zeit.
  if(fs.existsSync(dir+'/lipsync.mp4')){const cache=`${dir}/_loop_sync`;
    if(!fs.existsSync(cache+'/0000.png'))execFileSync('python3',[path.join(A,'..','engine','avatar','key_loop.py'),dir+'/lipsync.mp4',cache],{stdio:'inherit'});
    loops.sync=fs.readdirSync(cache).filter(x=>x.endsWith('.png')).sort().map(x=>`${cache}/${x}`);}
  // Ping-Pong (vor, zurück, vor ...) mit zufälligem Startpunkt je Reel -> keine sichtbare Naht, nie identisch
  const pick=(nm,t)=>{const L=loops[nm];if(!L)return null;if(nm==='sync')return L[Math.min(L.length-1,Math.round(t*30))];const n=L.length,i=(seed+Math.round(t*30))%(2*n-2);return L[i<n?i:2*n-2-i];};
  const frameAt=async(t)=>{const nm=await p.evaluate(t=>window.loopNeeded?window.loopNeeded(t):null,t);const f=nm&&pick(nm,t);
    return p.evaluate(async([t,d])=>{if(d)await window.setLoop(d);return render(t);},[t,f?'data:image/png;base64,'+fs.readFileSync(f).toString('base64'):null]);};
  if(mode==='stills'){const ts=(process.env.TS||'0.1,1.5,3.6,5.3,8.9,10.5,12.6,15,17.8').split(',').map(Number);for(const t of ts){fs.writeFileSync(`${out}/s_${t}.jpg`,dec(await frameAt(t)));}await b.close();return;}
  const cues=await p.evaluate(()=>window.CUES||[]);
  const fps=30,dur=Math.round(END*30)/30,n=Math.round(fps*dur);const vid=dir+'/_video.mp4';
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',''+fps,'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',vid],{stdio:['pipe','inherit','inherit']});
  for(let i=0;i<n;i++){const d=await frameAt(i/fps);if(!ff.stdin.write(dec(d)))await new Promise(r=>ff.stdin.once('drain',r));}
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
