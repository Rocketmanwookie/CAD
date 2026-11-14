-- PostgreSQL baseline. Use a dedicated database and least-privilege roles.
CREATE TABLE IF NOT EXISTS asset (
  robot_id text PRIMARY KEY, manufacturer text NOT NULL, variant text NOT NULL,
  serial_number text, controller text, robotware text, installed_options jsonb NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS model_revision (
  revision text PRIMARY KEY, robot_id text NOT NULL REFERENCES asset,
  cad_sha256 text NOT NULL, calibration_sha256 text,
  created_at timestamptz NOT NULL DEFAULT now(), validation_state text NOT NULL,
  parameters jsonb NOT NULL DEFAULT '{}', UNIQUE(revision, robot_id)
);
CREATE TABLE IF NOT EXISTS telemetry (
  robot_id text NOT NULL REFERENCES asset, stream_id text NOT NULL, seq bigint NOT NULL,
  source_time_ns bigint NOT NULL, received_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  model_revision text NOT NULL,
  FOREIGN KEY(model_revision,robot_id) REFERENCES model_revision(revision,robot_id),
  source text NOT NULL, quality text NOT NULL, body jsonb NOT NULL,
  PRIMARY KEY(robot_id, stream_id, seq), CHECK(seq >= 0), CHECK(source_time_ns >= 0)
);
CREATE INDEX IF NOT EXISTS telemetry_asset_time ON telemetry(robot_id, source_time_ns);
CREATE TABLE IF NOT EXISTS maintenance_event (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, robot_id text NOT NULL REFERENCES asset,
  occurred_at timestamptz NOT NULL, component text NOT NULL,
  action text NOT NULL, technician_ref text, evidence_uri text, details jsonb NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS fault_event (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, robot_id text NOT NULL REFERENCES asset,
  occurred_at timestamptz NOT NULL, code text NOT NULL, severity text NOT NULL,
  resolved_at timestamptz, details jsonb NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS production_run (
  run_id text PRIMARY KEY, robot_id text NOT NULL REFERENCES asset,
  start_at timestamptz NOT NULL, end_at timestamptz, job_id text NOT NULL,
  tool_revision text, payload_kg double precision, environment jsonb NOT NULL DEFAULT '{}'
);
CREATE TABLE IF NOT EXISTS analytics_result (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, robot_id text NOT NULL REFERENCES asset,
  occurred_at timestamptz NOT NULL, algorithm_revision text NOT NULL,
  model_revision text NOT NULL REFERENCES model_revision(revision),
  run_id text REFERENCES production_run, metric text NOT NULL, value double precision,
  unit text NOT NULL, quality text NOT NULL, details jsonb NOT NULL DEFAULT '{}'
);
