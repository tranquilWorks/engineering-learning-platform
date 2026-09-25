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
2. `ELP-DSP-P01` through `ELP-DSP-P84` create exactly one complete native
   learner module, self-contained Python runtime, and passing source-equivalence
   record in numeric order. Portfolio Control aggregate authorization
   `ELP-DSP-P01-P84` permits those 84 internal gates to be integrated as one
   target commit and one pull request; the ordered evidence and stop conditions
   remain unchanged.
3. `ELP-DSP-G-PYTHON` reviews the complete course, all equivalence and residual
   numerical records, browser/accessibility evidence, and every MATLAB
   `not_run` or `failed` result before any aggregate readiness claim.

ELP-DSP-00 establishes 84 pending, zero converted, zero blocked, and zero
placeholders. Its framework catalog is three courses,
two implemented modules, and two interactive modules because the discovered
DSP course is still empty. It does not deliver, display, or claim any converted
DSP lesson.

The ELP-DSP-P01-P84 aggregate candidate has completed the ordered software
conversion with 84 converted, zero pending, zero blocked, and zero placeholders.
Its catalog has 84 DSP/Radar modules plus the two existing platform modules.
Merge readiness remains conditional on exact-head hosted backend, frontend,
and container CI plus human review; MATLAB, browser/accessibility, learner,
physical-radar, release, deployment, and production claims remain outside the
software evidence boundary.

A blocked item stops the ordered lane. No batch may skip forward, combine
items, create bulk placeholders, mutate the pinned source, or infer MATLAB,
learner, release, deployment, production, or physical-radar evidence from a
Python conversion.

This lane is a separately authorized direct conversion sequence. It does not
implement or satisfy the generic B020 ingestion tooling or B030 author-preview
milestones below.

### ELP-DSP-FIDELITY-P02-P10 — Incremental issue-441 repair

**Status:** Implemented and locally verified as the first fidelity-remediation group.

P02-P10 replace the shared generic runtime with nine distinct source-faithful
experiments and five independently formulated scenarios per item. The repair
ledger keeps P01 as the prior distinct conversion, marks P02-P10 repaired, and
marks P11-P84 pending. Course-level numerical verification, curriculum coverage,
and capstone integration remain blocked until later issue-441 batches repair the
remaining generic modules and separately close the competency and P84 capstone gates.

## ELP-GNC — Authorized Controls/GNC conversion lane

**Depends on:** ELP-DSP-P01-P84

Portfolio Control aggregate authorization `ELP-GNC-P01-P24` advances the
read-only Controls/GNC source to
`ffd6623ee2cf8ccd8599fffd935ef07370750fa3` and converts all 24 implemented
lessons through ordered internal gates P01–P24. The retained target is one
commit and one pull request, while every item preserves its own exact source
hashes, target digest, numeric evidence, two sweeps, failure/recovery case, and
coverage transition.

The completed software course merged at
`923a86ab79893bd939d88d275bdcb12a5a1ddad6` and adds 24 native interactive
modules without changing the generic platform or the merged DSP/Radar course.
Final catalog shape is four courses, 110 modules, and 110 interactive modules.
P24 is a software-only virtual HIL plant/protocol exercise; physical HIL/HWIL
and timing claims remain outside this lane.

This direct course-owned lane does not complete B020 ingestion tooling, B030
author preview, B050 isolated execution, B070 MATLAB adapters, or B080 release
readiness.

## ELP-ORG-IDENTITY — TranquilWorks namespace normalization

**Depends on:** ELP-GNC-P01-P24

Normalize the post-transfer GitHub owner from `kpbianco` to
`tranquilWorks` for Portfolio Control, Engineering Learning Platform, all 13
submodule URLs, imported-course provenance chains, tests, current
documentation, and retained transfer evidence.

This administrative lane preserves every gitlink SHA and every course
manifest, lesson, experiment, and expected/actual numeric evidence file.
DSP/Radar remains 84/84, Controls/GNC remains 24/24, and the catalog remains
4 / 110 / 110. No unfinished course is imported or implemented by this
administrative lane. The later Robotics authorization below is separate.

## ELP-ROB-MANIPULATION-P61-P65 — Robotics manipulation and task autonomy

**Status:** Implemented and locally verified in its isolated target batch.

**Depends on:** `ELP-ROB-PLANNING-P54-P60`

This issue-440 batch implements grasp force closure, perception-guided pick/place, mobile-manipulator coordination, task-and-motion recovery, and multi-robot space-time reservations. It advances the course to 65 interactive modules and the platform catalog to 219 interactive modules. P66-P69 are delivered by the final systems/capstones batch below.

## ELP-ROB-SYSTEMS-CAPSTONES-P66-P69 — Robotics systems and capstones

**Status:** Implemented and locally verified in the final issue-440 target batch.

**Depends on:** `ELP-ROB-MANIPULATION-P61-P65`

This final batch implements typed model/frame/interface integration, deterministic timed replay with diagnosis and recovery, and two requirements-traced cumulative software capstones. Robotics closes at 69 interactive modules and the five-course catalog at 223 interactive modules. Curriculum coverage and software capstone integration pass; learner, MATLAB, browser/accessibility, and physical HIL validation remain unperformed.

## ELP-ROB — Authorized Robotics P01-P24 native Python lane

**Depends on:** ELP-ORG-IDENTITY

Portfolio Control batch `ELP-ROB-P01-P24` keeps the pinned
`robotics-autonomy-learning` source gitlink read-only at
`f8807640258f1a6c1c77f1dcc9e61734551c585b` and adds a separate
platform-owned `robotics-autonomy` course.

P01 retains and independently checks the implemented differential-drive source
design. P02-P24 retain their curriculum IDs, titles, questions, prerequisite
order, and source scaffold hashes, but their math and experiments are new
Python-first designs because the source items are non-runnable scaffolds.
NumPy supplies bounded calculations and Plotly JSON supplies the browser plots.
Independent analytic, invariant, continuous-time, or separately formulated
references check baseline and broken cases without importing production
experiments.

This batch ends at Robotics coverage 24 authored / 0 remaining / 0 blocked /
0 placeholders and catalog 5 / 134 / 134. P24 is software-only HIL methodology
and simulation, not physical HIL evidence. MATLAB runtime parity stays
`not_run`; no browser/accessibility, learner, physical robot/HIL, bench, field,
release, deployment, credential/settings, or production result is claimed.

## ELP-COURSE-CALIBER — Curriculum quality gate

**Depends on:** ELP-ROB-P01-P24

`ELP-COURSE-CALIBER-00` corrects the roadmap boundary after the initial course
conversions. The catalog totals—five courses, 134 modules, and 134 interactive
modules—remain implementation inventory only. They do not certify curriculum
coverage, capstone integration, or learner validation.

All new conversion and expansion work now requires a reviewed
competency-to-module matrix, a module count derived from that matrix, coherent
batches of no more than ten new lessons, semantic anti-template review, and
independently originated evidence. The six-stage and nine-dimension review is
defined in `docs/COURSE_CALIBER.md` and projected in
`docs/course-caliber-status.yaml`.

The audit itself created no child implementation. Controls/GNC fidelity (#438)
is completed by the separately authorized remediation below. Controls/GNC
expansion (#439), Robotics expansion (#440), and DSP/Radar fidelity (#441)
remain separately owned work. Vehicle Dynamics preparation is now separately
authorized under issue #467; lesson work still requires its own coherent
at-most-ten-lesson batch.

## ELP-GNC-FIDELITY — Controls/GNC P01-P24 remediation

**Depends on:** ELP-COURSE-CALIBER-00

Issue #438 repairs the existing 24-item Controls/GNC implementation without
adding curriculum. Every item retains exact source identity, a semantic map,
two one-variable sweeps, a named broken/recovery path, limiting cases, explicit
omissions, domain-specific axes, and five independently originated numerical
comparisons. P01 uses the pinned source's explicit-Euler failure step; P24 uses
two timestamped transport directions and source-ordered same-tick delivery.

Controls/GNC advances to `numerically_verified: passed` at a deterministic
software-only boundary. Curriculum coverage and capstone integration remain
partial, learner validation remains unperformed, and issue #439 is the sole
owner of later Controls/GNC expansion. The batch does not execute MATLAB,
validate browser accessibility or learners, operate physical HIL, or authorize
release, deployment, credentials/settings, or production use.

## ELP-GNC-EXPANSION — Competency-derived Controls/GNC P25-P68

**Depends on:** ELP-GNC-FIDELITY-P01-P24

Issue #439 derives a 68-module course from a reviewed competency and prerequisite map rather than a fixed lesson quota. The 44 native Python additions are divided into coherent batches of 9, 9, 9, 5, 6, 3, and 3 lessons. P25-P68 now implement the complete mapped sequence, including three requirements-traced cumulative capstones, with independent five-scenario evidence.

The final three lessons are cumulative capstones: identification/control/estimation under uncertainty; navigation/guidance of a constrained survey; and a requirements-traced faulted software-HIL GNC loop. Every issue-439 batch and capstone is implemented and locally verified. Native additions do not claim MATLAB/source equivalence, and the entire lane remains software-only.

## ELP-VEHICLE-PREP-00 — Vehicle Dynamics governed preparation

**Status:** Complete; P01-P67 implemented in eight separately authorized batches.

**Depends on:** `ELP-ROB-SYSTEMS-CAPSTONES-P66-P69`

Issue #467 derives 67 modules from the reviewed competency graph and partitions
them into eight coherent batches of at most ten lessons. This prep batch advances
only the read-only source gitlink, installs the exact 24-item source and coverage
ledgers, mirrors the reviewed map, and adds deterministic synthetic GR86
CAN/RaceChrono BLE protocol fixtures with independent decode and fault checks.

The completed implementation catalog has six courses, 290 modules, and 290 interactive modules;
Vehicle Dynamics contributes P01-P67. The fixture and all identification inputs are synthetic, not measured vehicle
data, and do not validate firmware, radio, bench, vehicle, track, or physical
HIL behavior. `ELP-VEHICLE-P01-P08`, `ELP-VEHICLE-P09-P16`, and
`ELP-VEHICLE-P17-P24`, `ELP-VEHICLE-TIRES-P25-P33`, and
`ELP-VEHICLE-CHASSIS-P34-P43`, `ELP-VEHICLE-PROPULSION-P44-P52`, and `ELP-VEHICLE-TELEMETRY-P53-P60` each have exact Portfolio Control authorization against
their merged predecessor. P01-P60 now
provide distinct bounded models, independent scalar references, five-scenario
evidence, named failures, and exact recoveries. P20 is explicitly a synthetic
offline stand-in despite its retained title, and P24 is a software-only GR86
baseline. P25-P33 deepen tire competencies; P34-P43 deepen handling, stability,
load-transfer, ride, damping, suspension, and anti-geometry competencies. P44-P52
deepen traction, launch, differential, gearing, braking, aero-balance, and stint-limit
competencies without altering the source-bound ledger. P53-P60 deepen telemetry replay, timing, calibration, reconstruction, estimation, identification, uncertainty, and fault recovery. P61-P67 close performance analysis and two cumulative capstones.

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

For courses outside the dedicated DSP/Radar and Controls/GNC lanes, migrate representative
modules before attempting every course:

1. one 3-D/heatmap-heavy engineering module;
2. one static/media-heavy module;
3. one course that stresses large data transport.

Use those pilots to revise the schema and authoring workflow before bulk conversion.
The separate ELP-DSP sequence above does not mark B020, B030, or this broader
cross-course migration milestone complete.
