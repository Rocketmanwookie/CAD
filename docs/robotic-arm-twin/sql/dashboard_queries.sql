-- Grafana PostgreSQL time-series query, joint 1 temperature; nanosecond epoch -> timestamp.
SELECT to_timestamp(source_time_ns / 1e9) AS "time",
       (body->'temperature'->>0)::double precision AS temperature_degC
FROM telemetry
WHERE robot_id = 'teaching_arm'
  AND source_time_ns BETWEEN (extract(epoch FROM $__timeFrom())*1e9)::bigint
                         AND (extract(epoch FROM $__timeTo())*1e9)::bigint
  AND quality = 'good'
ORDER BY source_time_ns;

-- Data-age query: Grafana displays this independently of the latest signal value.
SELECT extract(epoch FROM (clock_timestamp() - to_timestamp(max(source_time_ns)/1e9))) AS source_age_seconds
FROM telemetry WHERE robot_id = 'teaching_arm';

-- History/context query; adapt your time range in Grafana.
SELECT occurred_at, component, action, evidence_uri FROM maintenance_event
WHERE robot_id = 'teaching_arm' ORDER BY occurred_at DESC LIMIT 100;
