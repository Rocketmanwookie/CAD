#!/usr/bin/env python3
"""Open-source teaching lab: synthetic telemetry, validation, SQLite, replay, HTTP.
No hardware writes. Python standard library only. See GUIDE.md before using data.
"""
import argparse
import errno
import json
import math
import sqlite3
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOINTS = [f'joint_{i}' for i in range(1, 7)]


def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def validate(s):
    if not isinstance(s, dict):
        raise ValueError('Sample must be an object')
    for key in ('robot_id', 'stream_id', 'model_revision'):
        if not isinstance(s.get(key), str) or not s[key] or len(s[key]) > 128:
            raise ValueError('Missing/invalid ' + key)
    if s.get('schema_version') != 1 or type(s.get('schema_version')) is not int:
        raise ValueError('Unsupported schema')
    for key in ('seq', 'source_time_ns'):
        if type(s.get(key)) is not int or not 0 <= s[key] <= 2**63-1:
            raise ValueError('Expected nonnegative int64 ' + key)
    if s.get('joint_names') != JOINTS:
        raise ValueError('Wrong joint ordering')
    if s.get('source') not in ('synthetic', 'physical', 'replay'):
        raise ValueError('Invalid source')
    if s.get('mode') not in ('active', 'idle', 'fault'):
        raise ValueError('Invalid mode')
    if s.get('units') != {'q': 'rad', 'dq': 'rad/s', 'tau': 'N*m', 'temperature': 'degC'}:
        raise ValueError('Wrong units')
    if s.get('quality') not in ('good', 'uncertain', 'bad'):
        raise ValueError('Invalid quality')
    if not finite(s.get('clock_uncertainty_ms')) or s['clock_uncertainty_ms'] < 0:
        raise ValueError('Invalid clock uncertainty')
    for key in ('q', 'dq', 'tau', 'temperature'):
        v = s.get(key)
        if key != 'q' and v is None:
            continue  # unknown channels are unavailable, never fabricated zeros
        if not isinstance(v, list) or len(v) != 6 or not all(finite(x) for x in v):
            raise ValueError('Expected six finite values for ' + key)
    return s


def synthetic(seq, elapsed, stream):
    q = [0.3 * math.sin(elapsed * 0.7 + i * 0.4) for i in range(6)]
    return dict(schema_version=1, robot_id='teaching_arm', stream_id=stream,
        model_revision='EXAMPLE-NOT-MEASURED-v1', source='synthetic', seq=seq,
        source_time_ns=time.time_ns(), clock_uncertainty_ms=0.0,
        joint_names=JOINTS, q=q,
        dq=[0.21 * math.cos(elapsed * 0.7 + i * 0.4) for i in range(6)],
        tau=[2.0 * math.sin(elapsed * 0.7 + i * 0.4) for i in range(6)],
        temperature=[30 + 3 * math.sin(elapsed * .02 + i) for i in range(6)],
        mode='active', quality='good',
        units={'q': 'rad', 'dq': 'rad/s', 'tau': 'N*m', 'temperature': 'degC'})


class Store:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename, check_same_thread=False)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('''CREATE TABLE IF NOT EXISTS samples (
          robot TEXT, stream TEXT, seq INTEGER, source_ns INTEGER,
          receipt_ns INTEGER, body TEXT, PRIMARY KEY(robot,stream,seq))''')
        self.db.commit()
        self.lock = threading.Lock()
        self.latest = None
        self.latest_mono = None
        self.last_seq = {}
        self.duplicates = 0
        self.out_of_order = 0
        self.gaps = 0

    def add(self, s):
        validate(s)
        with self.lock:
            now_ns = time.time_ns()
            cur = self.db.execute('INSERT OR IGNORE INTO samples VALUES (?,?,?,?,?,?)',
                (s['robot_id'],s['stream_id'],s['seq'],s['source_time_ns'],now_ns,json.dumps(s)))
            self.db.commit()
            if cur.rowcount == 0:
                self.duplicates += 1
                return False
            key = (s['robot_id'], s['stream_id'])
            previous = self.last_seq.get(key)
            if previous is not None and s['seq'] <= previous:
                self.out_of_order += 1
                return False  # archived, but never moves the displayed state backward
            if previous is not None:
                self.gaps += max(0, s['seq'] - previous - 1)
            self.last_seq[key] = s['seq']
            self.latest = dict(s, receipt_time_ns=now_ns)
            self.latest_mono = time.monotonic()
            return True

    def status(self):
        with self.lock:
            age = None if self.latest_mono is None else time.monotonic() - self.latest_mono
            source_age = None if self.latest is None else (time.time_ns()-self.latest['source_time_ns'])/1e9
            stale = (age is None or age > .25 or source_age is None or source_age > .25 or source_age < -.05)
            usable = (not stale and self.latest['quality'] == 'good' and self.latest['clock_uncertainty_ms'] <= 5)
            return dict(sample=self.latest, receipt_age_s=age, source_age_s=source_age,
                        stale=stale, usable=usable, duplicates=self.duplicates,
                        out_of_order=self.out_of_order, sequence_gaps=self.gaps)

    def history(self):
        with self.lock:
            return [json.loads(x[0]) for x in self.db.execute(
                'SELECT body FROM samples ORDER BY receipt_ns DESC LIMIT 500')][::-1]


def generate(args):
    stream = str(uuid.uuid4())
    start_ns = time.time_ns() - round((args.count-1)/args.hz*1e9)
    with open(args.output, 'w') as f:
        for i in range(args.count):
            sample=synthetic(i, i / args.hz, stream)
            sample['source_time_ns']=start_ns+round(i/args.hz*1e9)
            f.write(json.dumps(sample) + '\n')
    print(f'Wrote {args.count} synthetic records to {args.output}')


def bind_server(port, handler):
    """Try the requested loopback port and up to four successive ports."""
    last_port = min(port + 4, 65535)
    for candidate in range(port, last_port + 1):
        try:
            return ThreadingHTTPServer(('127.0.0.1', candidate), handler)
        except OSError as exc:
            if exc.errno != errno.EADDRINUSE:
                raise
            print(f'Port {candidate} is already in use.', flush=True)
            if candidate == last_port:
                raise OSError(errno.EADDRINUSE,
                    f'Could not start teaching lab: ports {port}–{last_port} '
                    'are all in use. Choose another --port.') from exc


def serve(args):
    store = Store(args.database)
    stop = threading.Event()
    failures = []

    def producer():
        try:
            if args.replay:
                with open(args.replay) as f:
                    previous_ns = None
                    for line in f:
                        if stop.is_set(): break
                        s = validate(json.loads(line))
                        if previous_ns is not None:
                            delay = max(0, (s['source_time_ns'] - previous_ns) / 1e9 / args.speed)
                            if stop.wait(min(delay, 10)): break
                        previous_ns = s['source_time_ns']
                        # Preserve original source time; old replay is deliberately STALE.
                        store.add(dict(s, source='replay'))
            else:
                stream = str(uuid.uuid4()); start = time.monotonic(); seq = 0
                while not stop.is_set():
                    store.add(synthetic(seq, time.monotonic()-start, stream))
                    seq += 1
                    stop.wait(1 / args.hz)
        except Exception as exc:
            failures.append(str(exc))
            print('Producer stopped:', exc, flush=True)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path in ('/api/status', '/api/history'):
                data = store.status() if self.path.endswith('status') else store.history()
                if isinstance(data, dict): data['producer_errors'] = failures[:]
                body = json.dumps(data, allow_nan=False).encode(); kind = 'application/json'
            elif self.path in ('/cad.html', '/vibration.html', '/vibration-model.js', '/vibration-ui.js', '/maintenance.html', '/maintenance-model.js', '/maintenance-ui.js', '/cad_mesh.json', '/assets/abb_irb6720.glb', '/assets/abb_irb6720.obj', '/assets/abb_irb6720.mtl'):
                file = ROOT/'web'/self.path[1:]
                if not file.is_file():
                    self.send_error(404); return
                body=file.read_bytes(); kind={'.js':'text/javascript; charset=utf-8', '.json':'application/json', '.glb':'model/gltf-binary', '.obj':'text/plain; charset=utf-8', '.mtl':'text/plain; charset=utf-8'}.get(file.suffix,'text/html; charset=utf-8')
            elif self.path == '/':
                body = (ROOT/'web'/'index.html').read_bytes(); kind = 'text/html; charset=utf-8'
            else:
                self.send_error(404); return
            self.send_response(200); self.send_header('Content-Type', kind)
            self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(body)))
            self.end_headers(); self.wfile.write(body)

        def log_message(self, *_): pass

    try:
        server = bind_server(args.port, Handler)
    except OSError:
        store.db.close()
        raise
    thread = threading.Thread(target=producer, daemon=True); thread.start()
    actual_port = server.server_address[1]
    print(f'Teaching lab at http://127.0.0.1:{actual_port} (Ctrl+C stops)',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally:
        stop.set(); server.server_close(); thread.join(timeout=2)
        store.db.close()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    g = sub.add_parser('generate'); g.add_argument('--output',default='telemetry.jsonl')
    g.add_argument('--count',type=int,default=200); g.add_argument('--hz',type=float,default=100)
    s = sub.add_parser('serve'); s.add_argument('--database',default='/tmp/robot-twin-lab.sqlite')
    s.add_argument('--port',type=int,default=8765); s.add_argument('--hz',type=float,default=100)
    s.add_argument('--replay'); s.add_argument('--speed',type=float,default=1)
    args=p.parse_args()
    if args.command == 'serve' and not 1 <= args.port <= 65535:
        p.error('Port must be between 1 and 65535')
    if any(not math.isfinite(getattr(args,k,1)) or getattr(args,k,1)<=0 for k in ('hz','speed')) or getattr(args,'count',1)<1:
        p.error('Rates and count must be positive')
    try:
        (generate if args.command=='generate' else serve)(args)
    except OSError as exc:
        if exc.errno != errno.EADDRINUSE:
            raise
        p.exit(1, f'{exc.strerror}\n')


if __name__=='__main__': main()
