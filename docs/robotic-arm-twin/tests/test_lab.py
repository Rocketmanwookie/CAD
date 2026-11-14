"""Useful failure-path and mathematical checks for the standalone teaching code."""
import copy
import importlib.util
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT=Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'tools'/f'{name}.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
lab=load('twin_lab'); urdf=load('make_urdf')

class LabTests(unittest.TestCase):
    def test_busy_ports_try_next_and_return_bound_server(self):
        server = Mock()
        with patch.object(lab, 'ThreadingHTTPServer', side_effect=[
                OSError(lab.errno.EADDRINUSE, 'busy'),
                OSError(lab.errno.EADDRINUSE, 'busy'), server]) as factory:
            self.assertIs(lab.bind_server(8765, object), server)
        self.assertEqual([call.args[0][1] for call in factory.call_args_list],
                         [8765, 8766, 8767])

    def test_busy_ports_stop_after_five_total_attempts(self):
        with patch.object(lab, 'ThreadingHTTPServer',
                          side_effect=OSError(lab.errno.EADDRINUSE, 'busy')) as factory:
            with self.assertRaisesRegex(OSError, 'ports 8765–8769 are all in use'):
                lab.bind_server(8765, object)
        self.assertEqual(factory.call_count, 5)

    def test_port_retry_does_not_hide_other_errors(self):
        with patch.object(lab, 'ThreadingHTTPServer',
                          side_effect=PermissionError(lab.errno.EACCES, 'denied')) as factory:
            with self.assertRaises(PermissionError):
                lab.bind_server(8765, object)
        self.assertEqual(factory.call_count, 1)

    def test_port_retry_stops_at_last_valid_port(self):
        with patch.object(lab, 'ThreadingHTTPServer',
                          side_effect=OSError(lab.errno.EADDRINUSE, 'busy')) as factory:
            with self.assertRaises(OSError):
                lab.bind_server(65535, object)
        self.assertEqual(factory.call_count, 1)

    def sample(self,n=0): return lab.synthetic(n,n*.01,'test-stream')
    def test_bad_samples(self):
        for key,value in [('q',[0]*5),('q',[math.nan]*6),('seq',True),('source_time_ns',-1),('joint_names',list(reversed(lab.JOINTS))),('units',{}),('clock_uncertainty_ms',-1)]:
            with self.subTest(key=key,value=value):
                s=self.sample();s[key]=value
                with self.assertRaises(ValueError):lab.validate(s)
    def test_duplicate_order_gap_and_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=lab.Store(str(Path(tmp)/'db'))
            self.assertTrue(s.add(self.sample(0)))
            self.assertFalse(s.add(self.sample(0)))
            self.assertTrue(s.add(self.sample(3)))
            self.assertFalse(s.add(self.sample(2)))
            d=s.status();self.assertEqual(d['sample']['seq'],3)
            self.assertEqual((d['duplicates'],d['out_of_order'],d['sequence_gaps']),(1,1,2))
            self.assertEqual(len(s.history()),3);s.db.close()
    def test_stale_and_uncertain(self):
        s=lab.Store(':memory:');sample=self.sample();sample['source_time_ns']-=1_000_000_000
        s.add(sample);self.assertTrue(s.status()['stale'])
        sample=self.sample(1);sample['quality']='uncertain';s.add(sample)
        self.assertFalse(s.status()['usable']);s.latest_mono-=1
        self.assertTrue(s.status()['stale']);s.db.close()
    def test_missing_optional_channels_and_future_clock(self):
        sample=self.sample();sample.update(dq=None,tau=None,temperature=None)
        self.assertIs(lab.validate(sample),sample)
        s=lab.Store(':memory:');sample['source_time_ns']+=1_000_000_000
        s.add(sample);self.assertFalse(s.status()['usable']);s.db.close()

    def test_synthetic_velocity(self):
        t=.6;h=1e-5
        left=lab.synthetic(0,t-h,'s');right=lab.synthetic(0,t+h,'s');mid=lab.synthetic(0,t,'s')
        for a,b,v in zip(left['q'],right['q'],mid['dq']):self.assertAlmostEqual((b-a)/(2*h),v,places=8)
    def test_unmeasured_refused(self):
        with self.assertRaises(ValueError):urdf.build({'status':'unmeasured'})
    def test_example_six_joints(self):
        import json
        model=json.loads((ROOT/'config'/'example_model.json').read_text())
        root=urdf.ET.fromstring(urdf.build(model,True))
        self.assertEqual(len(root.findall("joint[@type='revolute']")),6)
        model['joints'][0]['axis']=[0,0,0]
        with self.assertRaises(ValueError):urdf.build(model,True)

if __name__=='__main__': unittest.main()
