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

ELP-B010-01 establishes the strict current v1 boundary, semantic reference
validation, deterministic content/Git/runtime identities, generated artifact
drift checks, and Git pin/revert recovery fixtures. Historical readers and
in-place migration remain intentionally absent; any later contract increment
requires its own reviewed batch.

## ELP-DSP — Authorized item-by-item DSP/Radar conversion lane

**Depends on:** ELP-B010-01

This direct, course-owned lane converts the pinned 84-item DSP/Radar source
without modifying it and without adding DSP-specific behavior to the generic
platform:

1. `ELP-DSP-00` pins source commit
   `5d73667a486df4a7b6c581e4c9406e810ed4f0f6`, records the immutable P01-P84
   mapping, and creates the empty native course plus conversion/evidence
   framework.
2. `ELP-DSP-P01` through `ELP-DSP-P84` each create exactly one complete native
   learner module, self-contained Python runtime, and passing source-equivalence
   record in numeric order.
3. `ELP-DSP-G-PYTHON` reviews the complete course, all equivalence and residual
   numerical records, browser/accessibility evidence, and every MATLAB
   `not_run` or `failed` result before any aggregate readiness claim.

ELP-DSP-00 establishes 84 pending, zero converted, zero blocked, and zero
placeholders. Its framework catalog is three courses,
two implemented modules, and two interactive modules because the discovered
DSP course is still empty. It does not deliver, display, or claim any converted
DSP lesson.

A blocked item stops the ordered lane. No batch may skip forward, combine
items, create bulk placeholders, mutate the pinned source, or infer MATLAB,
learner, release, deployment, production, or physical-radar evidence from a
Python conversion.

This lane is a separately authorized direct conversion sequence. It does not
implement or satisfy the generic B020 ingestion tooling or B030 author-preview
milestones below.

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

For courses outside the dedicated DSP/Radar lane, migrate representative
modules before attempting every course:

1. one controls/GNC module;
2. one 3-D/heatmap-heavy module from another engineering course;
3. one static/media-heavy module.

Use those pilots to revise the schema and authoring workflow before bulk conversion.
The separate ELP-DSP sequence above does not mark B020, B030, or this broader
cross-course migration milestone complete.
