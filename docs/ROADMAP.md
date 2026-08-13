# Delivery Roadmap

The roadmap is a dependency-ordered set of bounded batches suitable for Portfolio Control. Each batch must produce acceptance evidence and must not claim unperformed browser, MATLAB, security, or production validation.

## B000 — Foundation vertical slice

**Outcome:** One-port platform renders discovered courses and executes a real interactive radar lesson.

- React/Vite learner shell and responsive navigation;
- declarative lesson blocks and controls;
- Plotly renderer and dataframe table;
- FastAPI catalog/runtime;
- course/module schemas and templates;
- P30 echo-ranging vertical slice;
- advanced plotting showcase;
- deterministic backend tests;
- Docker/Compose deployment.

## B010 — Contract hardening

**Depends on:** B000

- complete JSON Schemas for every nested field;
- schema migration framework and fixtures;
- semantic validation for block output references;
- course revision metadata;
- compatibility tests for version-one courses;
- generated TypeScript types from the canonical schema.

## B020 — Course ingestion and migration tooling

**Depends on:** B010

- `elp inspect-course PATH` readiness report;
- MATLAB-first module inventory scanner;
- scaffold generator for `course.yaml`, `module.yaml`, and migration notes;
- golden-vector file convention;
- no-write dry-run by default;
- explicit author-owned apply mode.

## B030 — Author preview and component gallery

**Depends on:** B010

- live reload across mounted course directories;
- schema-aware author diagnostics in the browser;
- searchable component/plot gallery;
- responsive visual regression fixtures;
- accessibility regression suite;
- module state permalink/export.

## B040 — Large numerical data transport

**Depends on:** B010

- Apache Arrow IPC artifact endpoint;
- Parquet dataset references;
- bounded artifact lifetime and cleanup;
- server-side downsampling/tiling contracts;
- virtualized tables;
- large heatmap/range–Doppler performance tests.

## B050 — Isolated execution workers

**Depends on:** B010

- queue-backed subprocess/container worker;
- hard CPU/memory/wall-clock limits;
- no-network execution profile;
- result and artifact quotas;
- cancellation and stale-run suppression;
- concurrency/fairness tests;
- worker health and telemetry.

## B060 — Progress, assessments, and SSO

**Depends on:** B030, B050

- reverse-proxy identity contract;
- learner progress separate from canonical course content;
- prediction/check responses;
- completion and teach-back evidence;
- role model for learner, author, reviewer, administrator;
- export/delete/retention policy.

## B070 — Runtime adapters

**Depends on:** B050

- remote Python/GPU worker;
- optional MATLAB Engine worker with license/capacity controls;
- optional browser WASM kernels;
- adapter conformance tests against one result envelope;
- golden-vector parity reporting.

## B080 — Corporate release readiness

**Depends on:** B040, B050, B060

- deployment manifests for the chosen corporate platform;
- SBOM, signing, scans, and offline dependency mirroring;
- structured logging and OpenTelemetry;
- backup/restore for learner progress;
- load test and capacity envelope;
- rollback rehearsal;
- operations runbook.

## B090 — First course migrations

**Depends on:** B020, B030

Migrate representative modules before attempting every course:

1. DSP/radar P03 aliasing;
2. DSP/radar P30 echo ranging;
3. one 3-D/heatmap-heavy advanced radar module;
4. one controls/GNC module;
5. one static/media-heavy module.

Use those pilots to revise the schema and authoring workflow before bulk conversion.
