'use strict';
const assert=require('node:assert/strict'),M=require('../web/vibration-model.js');
const base={motorJ:.0002,ratio:100,loadJ:5,shaftK:20000,holdK:10000,motorB:20,loadB:2,shaftC:10,amplitude:1,frequency:5,duration:8,initialDeg:.1,excitation:'harmonic'};
function near(a,b,rel=1e-6){assert.ok(Math.abs(a-b)<=rel*Math.max(Math.abs(b),1e-10),`${a} != ${b}`)}
let dc=M.response(base,0);near(dc.motorAmplitude,1/base.holdK);near(dc.loadAmplitude,1/base.holdK);near(dc.twistAmplitude,0);
const exact={...base,motorJ:1,ratio:1,loadJ:1,shaftK:1,holdK:1,motorB:0,loadB:0,shaftC:0};let freqs=M.modes(exact);near(freqs[0],Math.sqrt((3-Math.sqrt(5))/2)/(2*Math.PI));near(freqs[1],Math.sqrt((3+Math.sqrt(5))/2)/(2*Math.PI));assert.throws(()=>M.response(exact,freqs[0]),/resonance/i);
let r=M.simulate(base);let window=r.rows.filter(x=>x[0]>=6),dt=window[1][0]-window[0][0],sin=0,cos=0;for(let i=0;i<window.length-1;i++){let a=window[i],b=window[i+1],h=b[0]-a[0];sin+=h*(a[2]*Math.sin(2*Math.PI*5*a[0])+b[2]*Math.sin(2*Math.PI*5*b[0]))/2;cos+=h*(a[2]*Math.cos(2*Math.PI*5*a[0])+b[2]*Math.cos(2*Math.PI*5*b[0]))/2;}near(2*Math.hypot(sin,cos)/(window.at(-1)[0]-window[0][0]),M.response(base,5).loadAmplitude,.015);
const ring=M.simulate({...base,excitation:'ringdown'});assert.ok(ring.finalEnergy<ring.initialEnergy*.05,'damping must dissipate free-response energy');
const noDamp=M.simulate({...base,excitation:'ringdown',motorB:0,loadB:0,shaftC:0});near(noDamp.finalEnergy,noDamp.initialEnergy,2e-5);
const zeros=M.simulate({...base,amplitude:0});assert.equal(zeros.peakLoad,0);
assert.throws(()=>M.simulate({...base,shaftK:-1}),/positive/);assert.throws(()=>M.simulate({...base,motorJ:Infinity}),/finite/);assert.throws(()=>M.simulate({...base,ratio:1e308}),/finite/);assert.throws(()=>M.simulate({...base,frequency:0}),/positive frequency/);
console.log('PASS: analytic modal frequencies, static compliance, harmonic numeric/analytic agreement, energy conservation/dissipation, zero input and invalid-parameter handling');
