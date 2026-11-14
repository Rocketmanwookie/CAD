"""Read validated JSONL on stdin and insert idempotently into PostgreSQL.
Install psycopg separately. Provision asset/model records first. No hardware writes.
For durable production MQTT delivery use an acknowledged consumer and edge spool;
a shell pipe plus mosquitto_sub does not establish database commit acknowledgments.
"""
import json
import os
import sys
from twin_lab import validate


def main():
    import psycopg
    from psycopg.types.json import Jsonb
    with psycopg.connect(os.environ['TWIN_DATABASE_DSN']) as db:
        for line_number,line in enumerate(sys.stdin,1):
            try:s=validate(json.loads(line))
            except (ValueError,TypeError) as e:
                print(f'Rejected line {line_number}: {e}',file=sys.stderr);continue
            with db.transaction():
                db.execute('''INSERT INTO telemetry
                    (robot_id,stream_id,seq,source_time_ns,model_revision,source,quality,body)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING''',
                    (s['robot_id'],s['stream_id'],s['seq'],s['source_time_ns'],
                     s['model_revision'],s['source'],s['quality'],Jsonb(s)))


if __name__=='__main__':main()
