/* MIT: two-inertia torsional model. All motor quantities referred to output side.
 * No ABB calibration or hardware control. CommonJS export supports numeric tests.
 */
(function(root){
'use strict';
const fields=['motorJ','ratio','loadJ','shaftK','holdK','motorB','loadB','shaftC','amplitude','frequency','duration','initialDeg'];
function validate(p){
 for(const k of fields)if(typeof p[k]!=='number'||!Number.isFinite(p[k]))throw Error(`Enter a finite number for ${k}.`);
 for(const k of ['motorJ','ratio','loadJ','shaftK','holdK','duration'])if(p[k]<=0)throw Error(`${k} must be positive.`);
 for(const k of ['motorB','loadB','shaftC','amplitude','frequency'])if(p[k]<0)throw Error(`${k} cannot be negative.`);
 if(p.duration>10||p.frequency>200||Math.abs(p.initialDeg)>2||p.amplitude>100)throw Error('Use duration ≤10 s, frequency ≤200 Hz, initial twist ≤2°, and torque ≤100 N·m.');
 if(p.excitation==='harmonic'&&p.frequency===0)throw Error('Periodic torque needs a positive frequency; zero-frequency input is not a sine excitation.');
 if(!['harmonic','ringdown'].includes(p.excitation))throw Error('Choose harmonic or ring-down excitation.');
 return p;
}
function matrices(p){validate(p);const m={jm:p.motorJ*p.ratio*p.ratio,jl:p.loadJ,k11:p.holdK+p.shaftK,k22:p.shaftK,k12:-p.shaftK,c11:p.motorB+p.shaftC,c22:p.loadB+p.shaftC,c12:-p.shaftC};if(!Object.values(m).every(Number.isFinite)||m.jm<=0)throw Error('Parameters exceed a finite physical model range.');return m;}
function modes(p){const m=matrices(p),a=m.k11/m.jm,d=m.k22/m.jl,b=m.k12/Math.sqrt(m.jm*m.jl),disc=Math.hypot(a-d,2*b),high=(a+d+disc)/2,low=(p.holdK*p.shaftK/(m.jm*m.jl))/high;if(!Number.isFinite(low)||!Number.isFinite(high)||low<=0||high<=0)throw Error('Natural frequencies are outside the numerical model range.');return [Math.sqrt(low)/(2*Math.PI),Math.sqrt(high)/(2*Math.PI)];}
const mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];
function divide(a,b){const size=Math.hypot(...b);if(size<1e-20)throw Error('Undamped resonance has no finite steady-state amplitude; add damping or change frequency.');const br=b[0]/size,bi=b[1]/size;return [(a[0]*br+a[1]*bi)/size,(a[1]*br-a[0]*bi)/size];}
function response(p,f){if(!Number.isFinite(f)||f<0)throw Error('Frequency must be nonnegative.');const m=matrices(p),w=2*Math.PI*f,a=[m.k11-m.jm*w*w,m.c11*w],d=[m.k22-m.jl*w*w,m.c22*w],b=[m.k12,m.c12*w],ad=mul(a,d),bb=mul(b,b),det=[ad[0]-bb[0],ad[1]-bb[1]];if(Math.hypot(...det)<1e-12*Math.max(Math.hypot(...ad),Math.hypot(...bb),1))throw Error('Undamped or singular resonance: no finite reliable steady-state response.');const motor=divide([p.amplitude*d[0],p.amplitude*d[1]],det),load=divide([-p.amplitude*b[0],-p.amplitude*b[1]],det);return {motor,load,motorAmplitude:Math.hypot(...motor),loadAmplitude:Math.hypot(...load),twistAmplitude:Math.hypot(motor[0]-load[0],motor[1]-load[1])};}
function derivative(m,p,t,y){const [qm,ql,vm,vl]=y,torque=p.excitation==='harmonic'?p.amplitude*Math.sin(2*Math.PI*p.frequency*t):0;return [vm,vl,(torque-m.c11*vm-m.c12*vl-m.k11*qm-m.k12*ql)/m.jm,(-m.c12*vm-m.c22*vl-m.k12*qm-m.k22*ql)/m.jl];}
function energy(m,y){return .5*(m.jm*y[2]**2+m.jl*y[3]**2+m.k11*y[0]**2+2*m.k12*y[0]*y[1]+m.k22*y[1]**2);}
function simulate(p){const m=matrices(p),natural=modes(p),fast=Math.max(natural[1],p.frequency,1),steps=Math.ceil(p.duration/Math.min(.001,1/(100*fast)));
 if(steps>200000)throw Error('This parameter combination needs too many integration steps. Reduce duration or stiffness, or increase inertia.');
 const dt=p.duration/steps,stride=Math.max(1,Math.ceil(steps/2400)),rows=[];let y=p.excitation==='ringdown'?[p.initialDeg*Math.PI/180,0,0,0]:[0,0,0,0],sum=0,peak=0,maxTwist=0,tailCount=0,tailSum=0;
 const initialEnergy=energy(m,y);for(let i=0;i<=steps;i++){let t=i*dt;peak=Math.max(peak,Math.abs(y[1]));maxTwist=Math.max(maxTwist,Math.abs(y[0]-y[1]));sum+=y[1]**2;if(i>=steps/2){tailSum+=y[1]**2;tailCount++;}if(i%stride===0||i===steps)rows.push([t,y[0],y[1],y[0]-y[1]]);if(i===steps)break;
 const k1=derivative(m,p,t,y),k2=derivative(m,p,t+dt/2,y.map((v,j)=>v+dt*k1[j]/2)),k3=derivative(m,p,t+dt/2,y.map((v,j)=>v+dt*k2[j]/2)),k4=derivative(m,p,t+dt,y.map((v,j)=>v+dt*k3[j]));y=y.map((v,j)=>v+dt*(k1[j]+2*k2[j]+2*k3[j]+k4[j])/6);if(!y.every(Number.isFinite))throw Error('Numerical response failed; check parameters.');}
 return {natural,dt,steps,rows,peakLoad:peak,rmsLoad:Math.sqrt(sum/(steps+1)),tailRmsLoad:Math.sqrt(tailSum/tailCount),peakTwist:maxTwist,initialEnergy,finalEnergy:energy(m,y)};
}
const api={validate,matrices,modes,response,simulate,energy};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.VibrationModel=api;
})(typeof globalThis!=='undefined'?globalThis:this);
