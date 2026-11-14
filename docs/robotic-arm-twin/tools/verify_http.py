"""Start a short-lived local server, verify endpoints, then stop it."""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as temp:
    proc=subprocess.Popen([sys.executable,str(root/'tools'/'twin_lab.py'),'serve',
        '--database',str(Path(temp)/'test.sqlite'),'--port','18765'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try:
        deadline=time.monotonic()+10
        while True:
            if proc.poll() is not None:raise RuntimeError(proc.stdout.read().decode())
            try:
                with urlopen('http://127.0.0.1:18765/api/status',timeout=1) as r:d=json.load(r)
                if d['sample'] is not None:break
            except URLError:pass
            if time.monotonic()>deadline:raise TimeoutError('Server not ready')
            time.sleep(.05)
        assert d['sample']['source']=='synthetic' and d['usable']
        for path,expected in [('/',b'Industrial arm twin'),('/cad.html',b'ABB IRB 6720'),('/vibration.html',b'Joint and motor vibration'),('/vibration-model.js',b'function simulate'),('/vibration-ui.js',b'function run'),('/maintenance.html',b'Maintenance timeline'),('/maintenance-model.js',b'function due'),('/maintenance-ui.js',b'function calculate'),('/cad_mesh.json',b'workspace excluded'),('/assets/abb_irb6720.glb',b'glTF'),('/assets/abb_irb6720.obj',b'mtllib abb_irb6720.mtl'),('/assets/abb_irb6720.mtl',b'newmtl body')]:
            with urlopen('http://127.0.0.1:18765'+path,timeout=5) as r:assert r.status==200 and expected in r.read()
        with urlopen('http://127.0.0.1:18765/api/history',timeout=1) as r:assert len(json.load(r))>0
        print('PASS: live synthetic state, freshness, history, HTML routes and CAD mesh HTTP delivery')
    finally:
        proc.terminate();proc.wait(timeout=5)
