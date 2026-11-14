// Browser-independent interaction checks using the actual page script.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const html=fs.readFileSync(path.join(__dirname,'../web/index.html'),'utf8');
class Element{
 constructor(){this.children=[];this.attributes={};this.events={};this.value='';this.textContent=''}
 append(child){this.children.push(child);if(child.selected)this.value=String(child.value)}
 replaceChildren(...children){this.children=children}
 setAttribute(key,value){this.attributes[key]=value}
 addEventListener(event,fn){this.events[event]=fn}
}
const elements={};const document={querySelector:s=>elements[s]??=(new Element()),getElementById:s=>elements['#'+s]??=(new Element()),createElement:()=>new Element()};
const context={document,console,setInterval:()=>{},fetch:async()=>{throw Error('offline test')}};
vm.createContext(context);vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
const shoulder=elements['#shoulder'],elbow=elements['#elbow'],arm=elements['#arm'];
assert.equal(shoulder.children.length,7);assert.equal(elbow.children.length,13);
const initial=arm.attributes.points;shoulder.value='0';elbow.value='0';shoulder.events.change();
assert.equal(arm.attributes.points,initial,'selection must wait for Go');
elements['#pose-form'].events.submit({preventDefault(){}});
assert.notEqual(arm.attributes.points,initial);
const flat=context.staticPose(0,0);
assert.ok(Math.abs(flat.holding[0]-8.829)<1e-10);
assert.ok(Math.abs(flat.holding[1]-3.924)<1e-10);
assert.ok(flat.deflection.every(x=>x<0),'gravity creates clockwise sag');
assert.ok(context.staticPose(90,0).holding.every(x=>Math.abs(x)<1e-10),'vertical load has zero horizontal moment arm');
for(let s=0;s<=90;s+=15)for(let e=-90;e<=90;e+=15){shoulder.value=String(s);elbow.value=String(e);elements['#pose-form'].events.submit({preventDefault(){}});assert.ok(!/NaN|Infinity/.test(arm.attributes.points));}
const last=arm.attributes.points;shoulder.value='999';elements['#pose-form'].events.submit({preventDefault(){}});assert.equal(arm.attributes.points,last);
assert.ok(!html.includes('<th>Temperature'));
assert.ok(!html.includes('Separate synthetic six-joint'));
assert.ok(!html.includes("fetch('/api/status')"));
console.log('PASS: dropdown increments, Go-only movement, 91 allowed poses, gravity reference cases, invalid-input rejection, no temperature column');
