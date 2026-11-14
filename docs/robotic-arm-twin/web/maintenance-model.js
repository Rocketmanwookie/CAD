/* MIT: schedule arithmetic and qualitative three-valued fault trees.
 * OEM intervals: ABB 3HAC085697-001 Rev N pp120-122. Scenarios are assumptions.
 */
(function(root){'use strict';
const tasks=[
{id:'seals',name:'Initial seal cleanup',kind:'once',hours:150,page:121,tree:'seal'},
{id:'clean',name:'Robot cleaning',kind:'condition',page:121,tree:'clean'},
{id:'balance',name:'Balancing-device inspection',kind:'calendar',months:12,page:121,tree:'balance'},
{id:'dampers',name:'Damper condition check',kind:'calendar',months:12,page:121,tree:'damper'},
{id:'labels',name:'Information-label inspection',kind:'calendar',months:12,page:121,tree:'label'},
{id:'stop',name:'Axis-1 stop inspection',kind:'calendar',months:12,page:121,tree:'stop'},
{id:'motorseal',name:'Motor-seal inspection',kind:'calendar',months:12,page:121,tree:'seal'},
{id:'oillevel',name:'Gearbox oil-level check',kind:'condition',page:121,tree:'oil'},
{id:'harness',name:'Cable-harness inspection',kind:'calendar',months:12,page:121,tree:'harness'},
...[1,2,3,4,5,6].map(i=>({id:'oil'+i,name:`Axis ${i} gearbox oil service`,kind:'hours',hours:20000,page:122,tree:'oil'})),
{id:'battery',name:'SMB battery renewal',kind:'calendar',months:36,page:122,tree:'battery'},
{id:'balancebearing',name:'Balancing-bearing lubrication',kind:'hours',hours:12000,page:122,tree:'balance'}];
function date(s){if(!/^\d{4}-\d{2}-\d{2}$/.test(s||''))throw Error('Enter an ISO calendar date.');let d=new Date(s+'T00:00:00Z');if(!Number.isFinite(+d)||d.toISOString().slice(0,10)!==s)throw Error('Invalid calendar date.');return d;}
function addMonths(s,n){let d=date(s),day=d.getUTCDate();d.setUTCDate(1);d.setUTCMonth(d.getUTCMonth()+n);let end=new Date(Date.UTC(d.getUTCFullYear(),d.getUTCMonth()+1,0)).getUTCDate();d.setUTCDate(Math.min(day,end));return d.toISOString().slice(0,10);}
function due(task,history,asof,currentHours,hoursPerDay){date(asof);if(currentHours!==null&&(!Number.isFinite(currentHours)||currentHours<0))throw Error('DTC must be nonnegative.');if(hoursPerDay!==null&&(!Number.isFinite(hoursPerDay)||hoursPerDay<=0||hoursPerDay>24))throw Error('Forecast DTC accrual must be >0 and ≤24 h/day.');
if(task.kind==='condition')return {status:'Condition-triggered / local plan',deadline:null};
if(task.kind==='calendar'){if(!history.lastDate)return {status:'Unknown — service date missing',deadline:null};if(date(history.lastDate)>date(asof))throw Error('Service date is after the as-of date.');let deadline=addMonths(history.lastDate,task.months);return {deadline,status:deadline<asof?'Overdue':deadline===asof?'Due today':'Scheduled'};}
if(task.kind==='once'&&history.completed===true)return {status:'Recorded complete',deadline:null};
if(task.kind==='once'&&history.completed!==false)return {status:'Unknown — completion history missing',deadline:null};
if(currentHours===null||task.kind==='hours'&&history.lastHours===null)return {status:'Unknown — DTC history missing',deadline:null};
if(task.kind==='hours'&&(!Number.isFinite(history.lastHours)||history.lastHours<0||history.lastHours>currentHours))throw Error('Last-service DTC must be between zero and current DTC.');
let next=task.kind==='once'?task.hours:history.lastHours+task.hours,remaining=next-currentHours,forecast=null;if(remaining>0&&hoursPerDay!==null){let d=date(asof);d.setUTCDate(d.getUTCDate()+Math.ceil(remaining/hoursPerDay));forecast=d.toISOString().slice(0,10)}return {deadline:`${next.toLocaleString('en-US')} DTC h`,remaining,forecast,status:remaining<0?'Overdue':remaining===0?'Due now':'Scheduled'};
}
function gate(kind,values){if(!['AND','OR'].includes(kind)||!values.length||!values.every(v=>[-1,0,1].includes(v)))throw Error('Invalid gate inputs.');return kind==='AND'?(values.includes(0)?0:values.includes(-1)?-1:1):(values.includes(1)?1:values.includes(-1)?-1:0);}
const leaf=(id,label)=>({id,label});const branch=(label,gate,...children)=>({label,gate,children});
const mechanisms={
oil:branch('Lubrication-related mechanical degradation','AND',leaf('lubricant','Lubricant condition/quantity is unsuitable'),leaf('load','Drive continues operating under load'),leaf('wear','Damaging wear develops without effective intervention')),
seal:branch('Unresolved sealing problem','AND',leaf('seal','Seal damage or a genuine leak exists'),leaf('unresolved','Leak/contamination remains unresolved'),leaf('load','Continued operation exposes the drive to adverse lubrication')),
balance:branch('Balancing system impairment','OR',branch('Mechanical balancing fault','AND',leaf('mechanical','Device or bearing condition deteriorates'),leaf('load','Arm loading makes that defect consequential')),branch('Lubrication-related bearing degradation','AND',leaf('lubrication','Bearing lubrication is inadequate'),leaf('cycles','Repeated loaded motion continues'),leaf('wear','Damage develops and is not corrected'))),
harness:branch('Cable-related interruption','AND',leaf('damage','Cable wear, cracking or restraint exists'),leaf('motion','Motion/contact aggravates the condition'),leaf('continuity','Power or signal continuity is impaired')),
battery:branch('Calibration-data retention problem','AND',leaf('battery','Battery is depleted or low warning is unresolved'),leaf('event','An event requiring retained measurement data occurs'),leaf('retention','Required retained data becomes unavailable')),
damper:branch('Reduced impact attenuation','AND',leaf('damage','A damper is damaged or degraded'),leaf('impact','A motion/impact event engages that damper')),
stop:branch('Mechanical travel-limiting function impaired','AND',leaf('damage','Mechanical stop is damaged or incorrectly retained'),leaf('demand','A demand occurs that relies on the stop')),
label:branch('Maintenance/operation error pathway','AND',leaf('label','Needed label is unreadable or missing'),leaf('task','A task relies on that information'),leaf('error','An error occurs despite other information and checks')),
clean:branch('Contamination-related impairment','OR',branch('Cable movement restricted','AND',leaf('debris','Debris accumulates around moving cables'),leaf('movement','Cable movement is restricted')),branch('Sealing affected','AND',leaf('contamination','Adverse contamination reaches a vulnerable seal'),leaf('damage','Leakage or damage develops')))};
function tree(task){return branch('Potential impairment associated with neglected maintenance','AND',leaf('missed','Relevant maintenance was missed or ineffective'),mechanisms[task.tree]);}
function evaluate(node,states){return node.children?gate(node.gate,node.children.map(n=>evaluate(n,states))):(states[node.id]??-1);}
const api={tasks,date,addMonths,due,gate,tree,evaluate};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.MaintenanceModel=api;
})(typeof globalThis!=='undefined'?globalThis:this);
