const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
(async()=>{const [mode,arg]=process.argv.slice(2);const w=+(process.env.W||1920),h=+(process.env.H||1080);
 const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:w,height:h}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto(`file://${__dirname}/film.html?w=${w}&h=${h}${process.env.POSTER?'&poster=1':''}`);await p.evaluate(()=>window.ready);
 if(mode==='stills'){const dir=process.env.DIR||'st';fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
  for(const t of arg.split(',').map(Number)){await p.evaluate(t=>renderFrame(t),t);await p.screenshot({path:`${dir}/${t.toFixed(2)}.jpg`,type:'jpeg',quality:85})}}
 else{const fps=60,N=fps*30;const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','60','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p',arg],{stdio:['pipe','inherit','inherit']});
  const S0=Math.round(+(process.env.START||0)*fps);
  for(let i=S0;i<N;i++){await p.evaluate(t=>renderFrame(t),i/fps);const buf=await p.screenshot({type:'jpeg',quality:95});
   if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%300===0)console.log(i)}
  ff.stdin.end();await new Promise(r=>ff.on('close',r));console.log('DONE')}
 if(errs.length)console.log('ERRORS',errs);await b.close()})();
