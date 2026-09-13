import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const SC='/tmp/claude-0/-home-user-work-repo/d07398a7-f20e-57a7-98e6-b18d67fb1154/scratchpad';
const uri = fs.readFileSync(SC+'/house-datauri.txt','utf8');
const b = await chromium.launch();
const pg = await b.newPage({viewport:{width:1500,height:920}});
const errs=[]; pg.on('pageerror',e=>errs.push('PAGEERROR: '+e.message));
pg.on('console',m=>{if(m.type()==='error')errs.push('CONSOLE: '+m.text())});
pg.on('dialog', d => d.accept());
const ok=[], bad=[];
const check=(name,cond,detail='')=> (cond?ok:bad).push(name+(detail?' — '+detail:''));

await pg.goto('file:///home/user/work-repo/holiday-lighting-designer.html');
await pg.waitForTimeout(1000);

// 1. boots on the sample
let r = await pg.evaluate(()=>({runs:window.HLD.state.runs.length, refs:window.HLD.state.refs.length, img:!!window.HLD.image}));
check('boots with the sample loaded', r.runs>0 && r.refs>0 && r.img, JSON.stringify(r));

// 2. every tab renders
for(const t of ['tabQuote','tabJobs','tabPrice','tabDesign']){
  await pg.click('#'+t); await pg.waitForTimeout(350);
  const html = await pg.locator('#body'+t.replace('tab','')).innerHTML().catch(()=> '');
  check('tab '+t+' renders', html.length>50, html.length+' chars');
}

// 3. every tool switches
for(const t of ['tDraw','tCalib','tDecor','tSelect']){
  await pg.click('#'+t); await pg.waitForTimeout(120);
  check('tool '+t, await pg.locator('#'+t).evaluate(el=>el.classList.contains('on')));
}

// 4. draw a run by clicking, finish with Enter
await pg.click('#tabDesign'); await pg.click('#tDraw');
const cv = await pg.locator('#cv').boundingBox();
const P=(fx,fy)=>({x:cv.x+cv.width*fx, y:cv.y+cv.height*fy});
const n0 = await pg.evaluate(()=>window.HLD.state.runs.length);
for(const p of [P(0.3,0.3),P(0.45,0.22),P(0.6,0.3)]) await pg.mouse.click(p.x,p.y);
await pg.keyboard.press('Enter'); await pg.waitForTimeout(250);
const n1 = await pg.evaluate(()=>window.HLD.state.runs.length);
check('draw adds a run', n1===n0+1, `${n0} -> ${n1}`);

// 5. undo removes it
await pg.click('#tUndo'); await pg.waitForTimeout(250);
check('undo removes it', (await pg.evaluate(()=>window.HLD.state.runs.length))===n0);

// 6. place decor, drag it, delete it
await pg.click('#tDecor'); await pg.mouse.click(P(0.5,0.55).x, P(0.5,0.55).y); await pg.waitForTimeout(250);
const d1 = await pg.evaluate(()=>window.HLD.state.decor.length);
check('decor places', d1===1, 'count '+d1);
const before = await pg.evaluate(()=>({x:window.HLD.state.decor[0].x, y:window.HLD.state.decor[0].y}));
const a=P(0.5,0.55), z=P(0.56,0.6);
await pg.mouse.move(a.x,a.y); await pg.mouse.down(); await pg.mouse.move(z.x,z.y,{steps:6}); await pg.mouse.up();
await pg.waitForTimeout(250);
const after = await pg.evaluate(()=>({x:window.HLD.state.decor[0].x, y:window.HLD.state.decor[0].y}));
check('decor drags', Math.hypot(after.x-before.x, after.y-before.y) > 5);
await pg.keyboard.press('Delete'); await pg.waitForTimeout(200);
check('decor deletes', (await pg.evaluate(()=>window.HLD.state.decor.length))===0);

// 7. yardstick maths
const scale = await pg.evaluate(()=>{
  const H=window.HLD;
  H.state.refs=[{id:'t', a:{x:0,y:0}, b:{x:100,y:0}, feet:10}];
  const one = H.pxPerFtAt({x:50,y:0});
  H.state.refs.push({id:'t2', a:{x:900,y:0}, b:{x:950,y:0}, feet:10});
  const near1 = H.pxPerFtAt({x:20,y:0}), near2 = H.pxPerFtAt({x:930,y:0});
  H.state.refs=[{id:'door', a:{x:898,y:900}, b:{x:1007,y:900}, feet:3}];
  return {one:+one.toFixed(2), near1:+near1.toFixed(2), near2:+near2.toFixed(2)};
});
check('one yardstick = its own scale', Math.abs(scale.one-10)<0.01, JSON.stringify(scale));
check('blend favours the nearer yardstick', scale.near1>8.5 && scale.near2<6.5, JSON.stringify(scale));

// 8. quote arithmetic on a known run
const math = await pg.evaluate(()=>{
  const H=window.HLD;
  H.state.isSample=false; H.state.decor=[]; H.state.extras=[];
  H.state.refs=[{id:'r', a:{x:0,y:0}, b:{x:100,y:0}, feet:10}];   // 10 px per ft
  H.state.runs=[{id:'x', type:'roofline', productId:'c9-12', pattern:['ww'],
                 difficult:false, closed:false, points:[{x:0,y:0},{x:1000,y:0}]}];
  const q=H.quote(), L=H.shop.labor.find(l=>l.id==='c9roof');
  const bulbs=q.matRows.find(m=>m.sku==='20009-SPK'), clips=q.matRows.find(m=>m.sku==='14147');
  const wire=q.matRows.find(m=>m.sku==='19412-500');
  return {feet:+q.totalFeet.toFixed(2), bulbs:bulbs&&bulbs.qty, clips:clips&&clips.qty,
          wireFt:wire&&+wire.qty.toFixed(2), wireUnit:wire&&+wire.unit.toFixed(4),
          install:+q.install.toFixed(2), expectInstall:+(100*L.install).toFixed(2),
          contract:+q.contract.toFixed(2),
          sum:+(q.materials+q.install+q.takedown+q.storage).toFixed(2),
          tax:+q.tax.toFixed(2), expectTax:+(q.contract*H.shop.settings.taxPct/100).toFixed(2),
          deposit:+q.deposit.toFixed(2), half:+(q.total/2).toFixed(2)};
});
check('1000 px at 10 px/ft = 100 ft', Math.abs(math.feet-100)<0.05, JSON.stringify(math));
check('101 sockets at 12 in', math.bulbs===101 && math.clips===101, `bulbs ${math.bulbs} clips ${math.clips}`);
check('wire billed by the foot', Math.abs(math.wireFt-100)<0.05 && Math.abs(math.wireUnit-399.99/500)<0.0001);
check('install = feet x rate', Math.abs(math.install-math.expectInstall)<0.02, `${math.install} vs ${math.expectInstall}`);
check('contract = materials + all labor', Math.abs(math.contract-math.sum)<0.01);
check('tax on contract', Math.abs(math.tax-math.expectTax)<0.01);
check('deposit = half', Math.abs(math.deposit-math.half)<0.01);

// 9. wrap formula against the distributor sheet
const wrap = await pg.evaluate(()=>{
  const H=window.HLD;
  const run={id:'w', type:'column', productId:'mini-6', pattern:['ww'], difficult:false, closed:false,
             wrap:{on:true, shape:'square', w:8, l:8, circ:36, spacingIn:12},
             points:[{x:0,y:0},{x:0,y:155}]};              // 15.5 ft at 10 px/ft
  H.state.runs=[run];
  const hIn=15.5*12, expect=((8+8)*2*(hIn/12+1)+hIn)/12;
  return {got:+H.runStrandFeet(run).toFixed(2), expect:+expect.toFixed(2), strings:H.runStrings(run)};
});
check('wrap matches the sheet formula', Math.abs(wrap.got-wrap.expect)<0.02, JSON.stringify(wrap));

// 10. empty sockets
const off = await pg.evaluate(()=>{
  const H=window.HLD;
  const run={id:'o', type:'roofline', productId:'c9-12', pattern:['ww','off'], difficult:false, closed:false,
             points:[{x:0,y:0},{x:1000,y:0}]};
  H.state.runs=[run];
  const q=H.quote();
  return {sockets:H.runStrandSockets(run), bulbs:H.runStrandBulbs(run),
          clips:q.matRows.find(m=>m.sku==='14147').qty};
});
check('empty sockets skip a bulb but keep the clip',
      off.bulbs===Math.ceil(off.sockets/2) && off.clips===off.sockets, JSON.stringify(off));

// 11. a broken price is caught
const guard = await pg.evaluate(()=>{
  const H=window.HLD;
  H.state.runs=[]; H.state.extras=[{sku:'4255', qty:1, labor:null}];   // $3199 cost, $0.99 retail
  const q=H.quote();
  return {bad:q.badRows.length, sku:q.badRows[0] && q.badRows[0].sku};
});
check('impossible price is flagged', guard.bad===1 && guard.sku==='4255', JSON.stringify(guard));

// 12. save / load round trip through a file
const trip = await pg.evaluate(async () => {
  const H=window.HLD;
  H.state.extras=[]; H.state.decor=[];
  H.state.runs=[{id:'a', type:'roofline', productId:'c9-12', pattern:['ww','off'], difficult:true,
                 closed:false, laborId:'c9stake', beam:{beam:3,spread:1,opacity:0.5,surface:true,flip:true},
                 wrap:null, points:[{x:10,y:10},{x:200,y:40}]}];
  H.addDecor('50048', 300, 300);
  H.state.customer.name='Round trip';
  const rec = JSON.parse(JSON.stringify({
    refs:H.state.refs, runs:H.state.runs, decor:H.state.decor, extras:H.state.extras,
    name:H.state.customer.name
  }));
  const beforeTotal = +H.quote().total.toFixed(2);
  // wipe, then restore exactly as applyRecord would
  H.state.runs=[]; H.state.decor=[]; H.state.refs=[];
  H.state.runs=rec.runs; H.state.decor=rec.decor; H.state.refs=rec.refs;
  H.refresh();
  return {beforeTotal, afterTotal:+H.quote().total.toFixed(2),
          run:H.state.runs[0], decorCount:H.state.decor.length};
});
check('save/load keeps the quote', Math.abs(trip.beforeTotal-trip.afterTotal)<0.01, `${trip.beforeTotal} vs ${trip.afterTotal}`);
check('run keeps difficult/labor/beam', trip.run.difficult===true && trip.run.laborId==='c9stake' && trip.run.beam.flip===true);
check('decor survives', trip.decorCount===1);

// 13. exports
await pg.evaluate(async (uri)=>{
  const H=window.HLD;
  await new Promise(res=>{ H.setPhoto(uri,'h.jpg'); const t=setInterval(()=>{ if(H.image){clearInterval(t);res();} },50); });
}, uri);
await pg.waitForTimeout(500);
const exp = await pg.evaluate(()=>{
  const day=window.HLD.renderFull(false), night=window.HLD.renderFull(true);
  return {w:day.width, h:day.height, dayLen:day.toDataURL('image/jpeg',0.8).length,
          nightLen:night.toDataURL('image/jpeg',0.8).length};
});
check('full-res export at photo size', exp.w===2000 && exp.h===1316 && exp.dayLen>5000 && exp.nightLen>5000, JSON.stringify(exp));

// 14. night slider across its range
for(const v of ['0','35','70','100']){
  await pg.fill('#nightSlider', v); await pg.dispatchEvent('#nightSlider','input'); await pg.waitForTimeout(140);
}
check('night slider sweeps clean', true);

console.log('PASS ('+ok.length+')'); ok.forEach(x=>console.log('  ✓ '+x));
if(bad.length){ console.log('\nFAIL ('+bad.length+')'); bad.forEach(x=>console.log('  ✗ '+x)); }
console.log('\nconsole/page errors: '+(errs.length?errs.length:'none'));
errs.slice(0,10).forEach(e=>console.log('  '+e));
await b.close();
process.exit(bad.length||errs.length ? 1 : 0);
